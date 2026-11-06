"""Étape 7 : limitation de débit, champ piège, changement de mot de passe."""


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


MESSAGE = {
    "name": "Awa Traoré",
    "phone": "+2250700000000",
    "subject": "Pédiatrie",
    "content": "Je souhaite un rendez-vous.",
    "urgency": "programme",
}


# ── Rate limiting ─────────────────────────────────────────


def test_login_is_rate_limited_after_8_attempts(client):
    for _ in range(8):
        response = client.post("/auth/login", json={"username": "admin", "password": "faux"})
        assert response.status_code == 401
    blocked = client.post("/auth/login", json={"username": "admin", "password": "faux"})
    assert blocked.status_code == 429
    assert int(blocked.headers["Retry-After"]) > 0
    # Even the right password is refused while blocked (brute-force protection).
    assert client.post("/auth/login", json={"username": "admin", "password": "admin123"}).status_code == 429


def test_contact_form_is_rate_limited(client):
    for _ in range(5):
        assert client.post("/api/messages", json=MESSAGE).status_code == 201
    assert client.post("/api/messages", json=MESSAGE).status_code == 429


def test_rate_limit_can_be_disabled(client, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "rate_limit_enabled", False)
    for _ in range(7):
        assert client.post("/api/messages", json=MESSAGE).status_code == 201


def test_rate_limiter_window_expires():
    from app.rate_limit import SlidingWindowLimiter

    now = [1000.0]  # fake clock (real sleeps are flaky: ~15 ms timer steps on Windows)
    limiter = SlidingWindowLimiter(clock=lambda: now[0])
    assert limiter.hit("k", 2, 60) is None
    assert limiter.hit("k", 2, 60) is None
    assert limiter.hit("k", 2, 60) == 61  # blocked, wait the full window
    now[0] += 30
    assert limiter.hit("k", 2, 60) == 31  # still blocked
    now[0] += 31
    assert limiter.hit("k", 2, 60) is None  # window passed
    assert limiter.hit("other", 2, 60) is None  # keys are independent


# ── Honeypot ──────────────────────────────────────────────


def test_contact_honeypot_rejects_bots_and_is_never_stored(client, admin_token):
    bot = client.post("/api/messages", json={**MESSAGE, "website": "http://spam.example"})
    assert bot.status_code == 400

    human = client.post("/api/messages", json={**MESSAGE, "website": ""})
    assert human.status_code == 201
    assert "website" not in human.json()

    stored = client.get("/api/messages", headers=auth_headers(admin_token)).json()
    assert len(stored) == 1


def test_application_honeypot_rejects_bots(client, admin_token):
    offer = client.post(
        "/api/jobs/offers", json={"title": "Sage-femme", "contract_type": "CDI"}, headers=auth_headers(admin_token)
    ).json()
    data = {
        "first_name": "Awa",
        "last_name": "Traoré",
        "email": "awa.traore@email.ci",
        "phone": "+2250700000000",
        "consent": "true",
        "website": "http://spam.example",
    }
    files = {"cv": ("cv.pdf", b"%PDF-1.4 fake", "application/pdf")}
    response = client.post(f"/api/jobs/offers/{offer['slug']}/applications", data=data, files=files)
    assert response.status_code == 400


# ── Password change ───────────────────────────────────────


def _change(client, token, current, new):
    return client.post(
        "/auth/change-password",
        json={"current_password": current, "new_password": new},
        headers=auth_headers(token),
    )


def test_change_password_requires_authentication(client):
    response = client.post("/auth/change-password", json={"current_password": "admin123", "new_password": "x"})
    assert response.status_code == 401


def test_change_password_rejects_wrong_current_password(client, admin_token):
    assert _change(client, admin_token, "pas-le-bon", "NouveauMotDePasse2026").status_code == 400


def test_change_password_rejects_weak_passwords(client, admin_token):
    assert _change(client, admin_token, "admin123", "court1").status_code == 422  # too short
    assert _change(client, admin_token, "admin123", "seulementdeslettres").status_code == 422  # no digit
    assert _change(client, admin_token, "admin123", "1234567890").status_code == 422  # no letter + common
    assert _change(client, admin_token, "admin123", "admin123").status_code == 422  # same as current


def test_change_password_success_replaces_old_password(client, admin_token):
    assert _change(client, admin_token, "admin123", "Clinique-Sviateur-2026").status_code == 204
    assert client.post("/auth/login", json={"username": "admin", "password": "admin123"}).status_code == 401
    assert (
        client.post("/auth/login", json={"username": "admin", "password": "Clinique-Sviateur-2026"}).status_code
        == 200
    )


def test_default_password_detection(client):
    from app.auth.service import uses_default_password
    from app.database import get_db
    from app.main import app

    db = next(app.dependency_overrides[get_db]())
    assert uses_default_password(db) is True
