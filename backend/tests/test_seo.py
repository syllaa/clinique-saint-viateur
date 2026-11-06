"""Étape 8 : sitemap.xml et robots.txt."""


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_sitemap_lists_only_public_content(client, admin_token, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "site_url", "https://www.exemple-clinique.ci/")
    h = auth_headers(admin_token)

    active = client.post("/api/specialties", json={"name": "Cardiologie"}, headers=h).json()
    hidden = client.post("/api/specialties", json={"name": "Neurologie"}, headers=h).json()
    client.patch(f"/api/specialties/{hidden['id']}/toggle-active", headers=h)

    category = client.post("/api/blog/categories", json={"name": "Prévention"}, headers=h).json()
    client.post(
        "/api/blog/articles",
        json={"title": "Article publié", "excerpt": "x", "category_id": category["id"], "status": "published"},
        headers=h,
    )
    client.post(
        "/api/blog/articles",
        json={"title": "Brouillon secret", "excerpt": "x", "category_id": category["id"], "status": "draft"},
        headers=h,
    )
    client.post("/api/jobs/offers", json={"title": "Sage-femme", "contract_type": "CDI"}, headers=h)

    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    xml = response.text
    assert xml.startswith('<?xml version="1.0" encoding="UTF-8"?>')

    base = "https://www.exemple-clinique.ci"
    assert f"<loc>{base}/</loc>" in xml  # no double slash
    assert f"<loc>{base}/specialites/{active['slug']}</loc>" in xml
    assert f"/specialites/{hidden['slug']}<" not in xml
    assert f"<loc>{base}/blog/article-publie</loc>" in xml
    assert "brouillon-secret" not in xml
    assert f"<loc>{base}/nous-rejoindre/offres/sage-femme</loc>" in xml
    assert "/admin" not in xml and "/login" not in xml


def test_robots_points_to_sitemap(client, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "site_url", "https://www.exemple-clinique.ci")
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert "User-agent: *" in response.text
    assert "Sitemap: https://www.exemple-clinique.ci/sitemap.xml" in response.text
    assert "admin" not in response.text.lower()
