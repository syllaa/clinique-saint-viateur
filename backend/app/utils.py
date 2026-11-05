import re
import unicodedata
from typing import Callable

import nh3


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "item"


def unique_slug(base: str, exists: Callable[[str], bool]) -> str:
    """Slugify `base`, appending -2, -3, ... until `exists(candidate)` is False."""
    slug = slugify(base)
    candidate = slug
    n = 2
    while exists(candidate):
        candidate = f"{slug}-{n}"
        n += 1
    return candidate


_ALLOWED_HTML_TAGS = {"p", "br", "strong", "em", "u", "ul", "ol", "li", "h2", "h3", "a", "blockquote"}
# nh3 auto-manages the "rel" attribute on <a> tags (adds a safe noopener/noreferrer
# value); whitelisting it ourselves would conflict with that, hence it's absent here.
_ALLOWED_HTML_ATTRIBUTES = {"a": {"href", "target"}}


def sanitize_html(value: str) -> str:
    """Strip any HTML outside a small safe allow-list, used for any admin-authored
    rich-text field (blog articles, job offer descriptions) rendered via v-html."""
    return nh3.clean(value, tags=_ALLOWED_HTML_TAGS, attributes=_ALLOWED_HTML_ATTRIBUTES)
