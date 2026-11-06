"""Étape 7 : upload de vidéos et vidéo de couverture des spécialités."""

MP4 = b"\x00\x00\x00\x18ftypisom\x00\x00\x02\x00isomiso2" + b"\x00" * 64
WEBM = b"\x1a\x45\xdf\xa3" + b"\x9f\x42\x86\x81\x01" + b"\x00" * 64


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def _upload(client, token, name, content, mime="video/mp4"):
    return client.post("/api/uploads/videos", files={"file": (name, content, mime)}, headers=auth_headers(token))


def test_video_upload_requires_admin(client, isolated_uploads):
    assert client.post("/api/uploads/videos", files={"file": ("a.mp4", MP4, "video/mp4")}).status_code == 401


def test_valid_mp4_and_webm_are_stored(client, admin_token, isolated_uploads):
    mp4 = _upload(client, admin_token, "clip.mp4", MP4)
    assert mp4.status_code == 200
    assert mp4.json()["url"].startswith("/uploads/videos/") and mp4.json()["url"].endswith(".mp4")

    webm = _upload(client, admin_token, "clip.webm", WEBM, "video/webm")
    assert webm.status_code == 200
    assert webm.json()["url"].endswith(".webm")

    stored = sorted(p.suffix for p in (isolated_uploads / "videos").iterdir())
    assert stored == [".mp4", ".webm"]


def test_disallowed_extension_rejected(client, admin_token, isolated_uploads):
    assert _upload(client, admin_token, "clip.avi", MP4, "video/x-msvideo").status_code == 422


def test_renamed_file_rejected_by_signature(client, admin_token, isolated_uploads):
    """A non-video renamed .mp4 is refused: the content is checked, not just the name."""
    assert _upload(client, admin_token, "clip.mp4", b"MZ this is an exe" + b"\x00" * 32).status_code == 422
    assert _upload(client, admin_token, "clip.webm", MP4, "video/webm").status_code == 422


def test_video_size_limit(client, admin_token, isolated_uploads, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "max_video_mb", 1)
    too_big = MP4 + b"\x00" * (1024 * 1024)
    assert _upload(client, admin_token, "clip.mp4", too_big).status_code == 422


def test_specialty_rejects_external_video_url(client, admin_token, isolated_uploads):
    response = client.post(
        "/api/specialties",
        json={"name": "Cardiologie", "cover_video_url": "https://exemple.com/video.mp4"},
        headers=auth_headers(admin_token),
    )
    assert response.status_code == 422


def test_specialty_video_lifecycle_cleans_up_files(client, admin_token, isolated_uploads):
    videos = isolated_uploads / "videos"
    first = _upload(client, admin_token, "a.mp4", MP4).json()["url"]
    specialty = client.post(
        "/api/specialties", json={"name": "Cardiologie", "cover_video_url": first}, headers=auth_headers(admin_token)
    ).json()
    assert specialty["cover_video_url"] == first

    # Public detail exposes the video.
    public = client.get(f"/api/specialties/{specialty['slug']}").json()
    assert public["cover_video_url"] == first

    # Replacing the video deletes the old file.
    second = _upload(client, admin_token, "b.webm", WEBM, "video/webm").json()["url"]
    client.patch(
        f"/api/specialties/{specialty['id']}", json={"cover_video_url": second}, headers=auth_headers(admin_token)
    )
    assert {p.name for p in videos.iterdir()} == {second.rsplit("/", 1)[1]}

    # Updating other fields keeps the video.
    client.patch(f"/api/specialties/{specialty['id']}", json={"description": "x"}, headers=auth_headers(admin_token))
    assert (videos / second.rsplit("/", 1)[1]).exists()

    # Removing it deletes the file too.
    removed = client.patch(
        f"/api/specialties/{specialty['id']}", json={"cover_video_url": None}, headers=auth_headers(admin_token)
    )
    assert removed.json()["cover_video_url"] is None
    assert list(videos.iterdir()) == []

    # Deleting a specialty deletes its video.
    third = _upload(client, admin_token, "c.mp4", MP4).json()["url"]
    client.patch(
        f"/api/specialties/{specialty['id']}", json={"cover_video_url": third}, headers=auth_headers(admin_token)
    )
    client.delete(f"/api/specialties/{specialty['id']}", headers=auth_headers(admin_token))
    assert list(videos.iterdir()) == []


def test_delete_helper_ignores_foreign_paths(isolated_uploads):
    """Only our own UUID-named files can be deleted (no path traversal)."""
    from app.uploads.service import delete_uploaded_video

    victim = isolated_uploads / "important.txt"
    victim.write_text("keep me")
    delete_uploaded_video("/uploads/videos/../important.txt")
    delete_uploaded_video("/uploads/images/abc.webp")
    assert victim.exists()
