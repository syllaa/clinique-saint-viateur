import io

from PIL import Image


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def _real_png_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (32, 32), color=(200, 30, 30)).save(buf, format="PNG")
    return buf.getvalue()


def test_valid_image_accepted_and_reencoded_as_webp(client, admin_token):
    response = client.post(
        "/api/uploads/images",
        files={"file": ("photo.png", _real_png_bytes(), "image/png")},
        headers=auth_headers(admin_token),
    )
    assert response.status_code == 200
    url = response.json()["url"]
    assert url.startswith("/uploads/images/")
    assert url.endswith(".webp")


def test_invalid_extension_rejected(client, admin_token):
    response = client.post(
        "/api/uploads/images",
        files={"file": ("script.exe", b"MZ", "application/octet-stream")},
        headers=auth_headers(admin_token),
    )
    assert response.status_code == 422


def test_fake_image_content_rejected_despite_valid_extension(client, admin_token):
    """A renamed non-image file must be caught even though its extension is allowed."""
    response = client.post(
        "/api/uploads/images",
        files={"file": ("photo.jpg", b"this is not actually an image", "image/jpeg")},
        headers=auth_headers(admin_token),
    )
    assert response.status_code == 422


def test_oversized_image_rejected(client, admin_token, monkeypatch):
    from app.uploads import service as uploads_service

    monkeypatch.setattr(uploads_service.settings, "max_image_mb", 0)
    response = client.post(
        "/api/uploads/images",
        files={"file": ("photo.jpg", _real_png_bytes(), "image/jpeg")},
        headers=auth_headers(admin_token),
    )
    assert response.status_code == 422


def test_upload_requires_admin(client):
    response = client.post("/api/uploads/images", files={"file": ("photo.jpg", b"x", "image/jpeg")})
    assert response.status_code == 401
