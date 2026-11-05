"""Minimal in-memory rate limiting for the public write endpoints.

Sliding window per (route name, client IP). No extra dependency.

Limits of this approach (documented on purpose):
- State lives in the process: with several uvicorn workers, each worker
  counts separately (the effective limit is multiplied by the worker
  count). Use a shared store (Redis) if the API is ever scaled out.
- Behind a reverse proxy, run uvicorn with --proxy-headers (and
  --forwarded-allow-ips) so request.client is the real visitor, not the
  proxy; otherwise every visitor shares one budget.
"""
import time
from collections import deque
from threading import Lock

from fastapi import HTTPException, Request, status

from app.config import get_settings


class SlidingWindowLimiter:
    PURGE_EVERY = 1000  # calls
    MAX_IDLE_SECONDS = 3600

    def __init__(self) -> None:
        self._hits: dict[str, deque[float]] = {}
        self._lock = Lock()
        self._calls = 0

    def _purge(self, now: float) -> None:
        """Drops visitors not seen for an hour, so memory stays bounded."""
        stale = [k for k, q in self._hits.items() if not q or q[-1] <= now - self.MAX_IDLE_SECONDS]
        for k in stale:
            del self._hits[k]

    def hit(self, key: str, limit: int, window_seconds: float) -> int | None:
        """Records one attempt. Returns None if allowed, else the number of
        seconds to wait before the next attempt is allowed."""
        now = time.monotonic()
        with self._lock:
            self._calls += 1
            if self._calls % self.PURGE_EVERY == 0:
                self._purge(now)
            hits = self._hits.setdefault(key, deque())
            while hits and hits[0] <= now - window_seconds:
                hits.popleft()
            if len(hits) >= limit:
                return int(hits[0] + window_seconds - now) + 1
            hits.append(now)
            return None

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()


limiter = SlidingWindowLimiter()


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def rate_limit(name: str, limit: int, window_seconds: float):
    """FastAPI dependency: `dependencies=[Depends(rate_limit("login", 8, 300))]`."""

    def dependency(request: Request) -> None:
        if not get_settings().rate_limit_enabled:
            return
        retry_after = limiter.hit(f"{name}:{_client_ip(request)}", limit, window_seconds)
        if retry_after is not None:
            raise HTTPException(
                status.HTTP_429_TOO_MANY_REQUESTS,
                "Trop de tentatives. Merci de patienter quelques minutes avant de réessayer.",
                headers={"Retry-After": str(retry_after)},
            )

    return dependency
