def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def create_category(client, admin_token, name="Prévention"):
    return client.post("/api/blog/categories", json={"name": name}, headers=auth_headers(admin_token)).json()


def test_category_crud_and_toggle(client, admin_token):
    category = create_category(client, admin_token, "Nutrition")
    assert category["slug"] == "nutrition"

    public = client.get("/api/blog/categories")
    assert any(c["id"] == category["id"] for c in public.json())

    toggled = client.patch(
        f"/api/blog/categories/{category['id']}/toggle-active", headers=auth_headers(admin_token)
    )
    assert toggled.json()["is_active"] is False
    assert all(c["id"] != category["id"] for c in client.get("/api/blog/categories").json())

    admin_all = client.get("/api/blog/categories/admin/all", headers=auth_headers(admin_token))
    assert any(c["id"] == category["id"] for c in admin_all.json())

    delete = client.delete(f"/api/blog/categories/{category['id']}", headers=auth_headers(admin_token))
    assert delete.status_code == 204


def test_article_publish_draft_and_slug(client, admin_token):
    category = create_category(client, admin_token, "Actualité")

    published = client.post(
        "/api/blog/articles",
        json={"title": "Article publié", "excerpt": "extrait", "category_id": category["id"], "status": "published"},
        headers=auth_headers(admin_token),
    )
    draft = client.post(
        "/api/blog/articles",
        json={"title": "Brouillon", "excerpt": "extrait", "category_id": category["id"], "status": "draft"},
        headers=auth_headers(admin_token),
    )
    assert published.status_code == 201
    assert published.json()["slug"] == "article-publie"
    assert published.json()["published_at"] is not None
    assert draft.json()["published_at"] is None

    public = client.get("/api/blog/articles")
    titles = [a["title"] for a in public.json()["items"]]
    assert "Article publié" in titles
    assert "Brouillon" not in titles

    # draft is invisible on the public detail route too
    assert client.get(f"/api/blog/articles/{draft.json()['slug']}").status_code == 404


def test_article_search_category_filter_and_pagination(client, admin_token):
    cat_a = create_category(client, admin_token, "Santé de l'enfant")
    cat_b = create_category(client, admin_token, "Cardiologie")

    for i in range(3):
        client.post(
            "/api/blog/articles",
            json={"title": f"Vaccination info {i}", "excerpt": "e", "category_id": cat_a["id"]},
            headers=auth_headers(admin_token),
        )
    client.post(
        "/api/blog/articles",
        json={"title": "Dépistage cardiaque", "excerpt": "e", "category_id": cat_b["id"]},
        headers=auth_headers(admin_token),
    )

    by_category = client.get(f"/api/blog/articles?category={cat_a['slug']}").json()
    assert by_category["total"] == 3
    assert all(a["category"]["slug"] == cat_a["slug"] for a in by_category["items"])

    by_search = client.get("/api/blog/articles?search=cardiaque").json()
    assert by_search["total"] == 1
    assert by_search["items"][0]["title"] == "Dépistage cardiaque"

    page1 = client.get(f"/api/blog/articles?category={cat_a['slug']}&page=1&page_size=2").json()
    assert len(page1["items"]) == 2
    page2 = client.get(f"/api/blog/articles?category={cat_a['slug']}&page=2&page_size=2").json()
    assert len(page2["items"]) == 1


def test_related_articles_exclude_self_and_match_category(client, admin_token):
    category = create_category(client, admin_token, "Bien-être")
    other_category = create_category(client, admin_token, "Conseils santé")

    main = client.post(
        "/api/blog/articles",
        json={"title": "Article principal", "excerpt": "e", "category_id": category["id"]},
        headers=auth_headers(admin_token),
    ).json()
    same_cat = client.post(
        "/api/blog/articles",
        json={"title": "Article similaire", "excerpt": "e", "category_id": category["id"]},
        headers=auth_headers(admin_token),
    ).json()
    client.post(
        "/api/blog/articles",
        json={"title": "Article autre categorie", "excerpt": "e", "category_id": other_category["id"]},
        headers=auth_headers(admin_token),
    )

    related = client.get(f"/api/blog/articles/{main['slug']}/related").json()
    related_titles = [a["title"] for a in related]
    assert same_cat["title"] in related_titles
    assert main["title"] not in related_titles
    assert "Article autre categorie" not in related_titles


def test_article_content_html_is_sanitized(client, admin_token):
    category = create_category(client, admin_token)
    created = client.post(
        "/api/blog/articles",
        json={
            "title": "Contenu riche",
            "excerpt": "e",
            "category_id": category["id"],
            "content": "<p>Texte <strong>important</strong></p><script>alert(1)</script>",
        },
        headers=auth_headers(admin_token),
    ).json()
    assert "<script>" not in created["content"]
    assert "<strong>important</strong>" in created["content"]


def test_article_mutations_require_admin(client):
    assert client.post("/api/blog/articles", json={"title": "x", "excerpt": "e", "category_id": 1}).status_code == 401
    assert client.get("/api/blog/articles/admin/all").status_code == 401


def test_article_structured_extras_roundtrip(client, admin_token):
    category = create_category(client, admin_token, "Événement")
    created = client.post(
        "/api/blog/articles",
        json={
            "title": "Campagne de dépistage",
            "excerpt": "e",
            "category_id": category["id"],
            "practical_info": "📅 29 septembre 2026\n🕐 8h – 16h",
            "included_items": "🩸 Tension artérielle\n📈 ECG",
            "benefits": "✅ Dépistage précoce\n🎁 Gratuité",
            "secondary_image_url": "/uploads/images/team.webp",
            "secondary_image_alt": "Équipe médicale",
        },
        headers=auth_headers(admin_token),
    ).json()
    assert created["practical_info"] == "📅 29 septembre 2026\n🕐 8h – 16h"
    assert created["included_items"] == "🩸 Tension artérielle\n📈 ECG"
    assert created["benefits"] == "✅ Dépistage précoce\n🎁 Gratuité"
    assert created["secondary_image_url"] == "/uploads/images/team.webp"
    assert created["secondary_image_alt"] == "Équipe médicale"
    assert created["faqs"] == []

    fetched = client.get(f"/api/blog/articles/{created['slug']}").json()
    assert fetched["practical_info"] == created["practical_info"]

    updated = client.patch(
        f"/api/blog/articles/{created['id']}",
        json={"benefits": "🎯 Nouveau bénéfice"},
        headers=auth_headers(admin_token),
    ).json()
    assert updated["benefits"] == "🎯 Nouveau bénéfice"
    assert updated["practical_info"] == created["practical_info"]  # untouched fields survive a partial update


def test_article_faq_nested_crud(client, admin_token):
    category = create_category(client, admin_token, "FAQ")
    article = client.post(
        "/api/blog/articles",
        json={"title": "Article avec FAQ", "excerpt": "e", "category_id": category["id"]},
        headers=auth_headers(admin_token),
    ).json()

    faq = client.post(
        f"/api/blog/articles/{article['id']}/faqs",
        json={"question": "Faut-il être à jeun ?", "answer": "Un jeûne de quelques heures est recommandé."},
        headers=auth_headers(admin_token),
    )
    assert faq.status_code == 201
    faq_id = faq.json()["id"]

    fetched = client.get(f"/api/blog/articles/{article['slug']}").json()
    assert len(fetched["faqs"]) == 1
    assert fetched["faqs"][0]["question"] == "Faut-il être à jeun ?"

    updated = client.patch(
        f"/api/blog/articles/faqs/{faq_id}",
        json={"answer": "Non, ce n'est pas nécessaire."},
        headers=auth_headers(admin_token),
    )
    assert updated.json()["answer"] == "Non, ce n'est pas nécessaire."

    delete = client.delete(f"/api/blog/articles/faqs/{faq_id}", headers=auth_headers(admin_token))
    assert delete.status_code == 204
    assert client.get(f"/api/blog/articles/{article['slug']}").json()["faqs"] == []


def test_article_faq_requires_admin_and_valid_article(client, admin_token):
    assert client.post("/api/blog/articles/1/faqs", json={"question": "q", "answer": "a"}).status_code == 401
    response = client.post(
        "/api/blog/articles/999999/faqs",
        json={"question": "q", "answer": "a"},
        headers=auth_headers(admin_token),
    )
    assert response.status_code == 404


def test_deleting_article_cascades_its_faqs(client, admin_token):
    category = create_category(client, admin_token, "Cascade")
    article = client.post(
        "/api/blog/articles",
        json={"title": "Article à supprimer", "excerpt": "e", "category_id": category["id"]},
        headers=auth_headers(admin_token),
    ).json()
    faq = client.post(
        f"/api/blog/articles/{article['id']}/faqs",
        json={"question": "q", "answer": "a"},
        headers=auth_headers(admin_token),
    ).json()

    client.delete(f"/api/blog/articles/{article['id']}", headers=auth_headers(admin_token))

    assert client.patch(
        f"/api/blog/articles/faqs/{faq['id']}", json={"answer": "x"}, headers=auth_headers(admin_token)
    ).status_code == 404
