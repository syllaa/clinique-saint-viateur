import shutil

import pytest

from app.backups import service


@pytest.fixture(autouse=True)
def isolated_backup_dir(tmp_path, monkeypatch):
    """Point backups at a throwaway directory so tests never touch the real
    backups/ folder, and clean it up afterwards regardless of outcome."""
    backup_dir = tmp_path / "backups"
    monkeypatch.setattr(service.settings, "backup_dir", str(backup_dir))
    yield
    shutil.rmtree(backup_dir, ignore_errors=True)


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_backup_mutations_require_admin(client):
    assert client.get("/api/backups").status_code == 401
    assert client.post("/api/backups").status_code == 401


def test_create_list_download_and_delete_backup(client, admin_token):
    created = client.post("/api/backups", headers=auth_headers(admin_token))
    assert created.status_code == 201
    body = created.json()
    assert body["filename"].startswith("backup_") and body["filename"].endswith(".sql")
    assert body["size_bytes"] > 0

    listed = client.get("/api/backups", headers=auth_headers(admin_token)).json()
    assert any(b["filename"] == body["filename"] for b in listed)

    download = client.get(f"/api/backups/{body['filename']}/download", headers=auth_headers(admin_token))
    assert download.status_code == 200
    assert len(download.content) == body["size_bytes"]

    delete = client.delete(f"/api/backups/{body['filename']}", headers=auth_headers(admin_token))
    assert delete.status_code == 204
    listed_after = client.get("/api/backups", headers=auth_headers(admin_token)).json()
    assert all(b["filename"] != body["filename"] for b in listed_after)


def test_download_rejects_invalid_filename(client, admin_token):
    response = client.get("/api/backups/../../etc/passwd/download", headers=auth_headers(admin_token))
    assert response.status_code in (404, 422)

    response = client.get("/api/backups/not-a-backup.sql/download", headers=auth_headers(admin_token))
    assert response.status_code == 404


def test_create_backup_fails_gracefully_with_bad_mysqldump_path(client, admin_token, monkeypatch):
    monkeypatch.setattr(service.settings, "mysqldump_path", "this-binary-does-not-exist")
    response = client.post("/api/backups", headers=auth_headers(admin_token))
    assert response.status_code == 502
