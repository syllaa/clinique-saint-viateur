from datetime import date, timedelta


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def create_promotion(client, admin_token, **overrides):
    payload = {
        "title": "Bilan de santé complet",
        "value_label": "-20%",
        "valid_until": (date.today() + timedelta(days=30)).isoformat(),
    }
    payload.update(overrides)
    return client.post("/api/promotions", json=payload, headers=auth_headers(admin_token)).json()


def test_promotion_crud_and_public_visibility(client, admin_token):
    promotion = create_promotion(client, admin_token)
    assert promotion["slug"] == "bilan-de-sante-complet"
    assert promotion["is_expired"] is False
    assert promotion["reaction_counts"] == {"like": 0, "interested": 0, "hot": 0, "not_interested": 0}

    public_list = client.get("/api/promotions").json()
    assert any(p["id"] == promotion["id"] for p in public_list)

    update = client.patch(
        f"/api/promotions/{promotion['id']}", json={"value_label": "-30%"}, headers=auth_headers(admin_token)
    )
    assert update.json()["value_label"] == "-30%"

    delete = client.delete(f"/api/promotions/{promotion['id']}", headers=auth_headers(admin_token))
    assert delete.status_code == 204
    assert not any(p["id"] == promotion["id"] for p in client.get("/api/promotions").json())


def test_unpublished_and_expired_promotions_hidden_from_active_list(client, admin_token):
    draft = create_promotion(client, admin_token, title="Offre brouillon", is_published=False)
    expired = create_promotion(
        client, admin_token, title="Offre expirée", valid_until=(date.today() - timedelta(days=1)).isoformat()
    )
    active = create_promotion(client, admin_token, title="Offre active")

    active_slugs = {p["slug"] for p in client.get("/api/promotions").json()}
    assert draft["slug"] not in active_slugs
    assert expired["slug"] not in active_slugs
    assert active["slug"] in active_slugs

    all_slugs = {p["slug"] for p in client.get("/api/promotions/all").json()["items"]}
    assert {draft["slug"], expired["slug"], active["slug"]} <= all_slugs

    admin_slugs = {p["slug"] for p in client.get("/api/promotions/admin/all", headers=auth_headers(admin_token)).json()}
    assert {draft["slug"], expired["slug"], active["slug"]} <= admin_slugs

    expired_entry = next(p for p in client.get("/api/promotions/all").json()["items"] if p["slug"] == expired["slug"])
    assert expired_entry["is_expired"] is True


def test_toggle_active(client, admin_token):
    promotion = create_promotion(client, admin_token)
    assert promotion["is_published"] is True

    toggled = client.patch(
        f"/api/promotions/{promotion['id']}/toggle-active", headers=auth_headers(admin_token)
    ).json()
    assert toggled["is_published"] is False

    active_slugs = {p["slug"] for p in client.get("/api/promotions").json()}
    assert promotion["slug"] not in active_slugs


def test_reaction_upsert_changes_existing_reaction(client, admin_token):
    promotion = create_promotion(client, admin_token)
    device_id = "device-abc-123"

    first = client.post(
        f"/api/promotions/{promotion['id']}/reactions", json={"device_id": device_id, "reaction_type": "like"}
    )
    assert first.status_code == 200
    assert first.json()["reaction_counts"]["like"] == 1
    assert first.json()["my_reaction"] == "like"

    changed = client.post(
        f"/api/promotions/{promotion['id']}/reactions", json={"device_id": device_id, "reaction_type": "hot"}
    )
    assert changed.status_code == 200
    counts = changed.json()["reaction_counts"]
    assert counts["hot"] == 1
    assert counts["like"] == 0
    assert changed.json()["my_reaction"] == "hot"

    fetched = client.get(f"/api/promotions?device_id={device_id}").json()
    mine = next(p for p in fetched if p["id"] == promotion["id"])
    assert mine["my_reaction"] == "hot"


def test_reaction_rejects_invalid_type(client, admin_token):
    promotion = create_promotion(client, admin_token)
    response = client.post(
        f"/api/promotions/{promotion['id']}/reactions",
        json={"device_id": "device-1", "reaction_type": "furious"},
    )
    assert response.status_code == 422


def test_reaction_rejected_on_expired_promotion(client, admin_token):
    promotion = create_promotion(
        client, admin_token, valid_until=(date.today() - timedelta(days=1)).isoformat()
    )
    response = client.post(
        f"/api/promotions/{promotion['id']}/reactions",
        json={"device_id": "device-1", "reaction_type": "like"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cette offre a expiré, vous ne pouvez plus réagir."


def test_reaction_rejected_on_unpublished_promotion(client, admin_token):
    promotion = create_promotion(client, admin_token, is_published=False)
    response = client.post(
        f"/api/promotions/{promotion['id']}/reactions",
        json={"device_id": "device-1", "reaction_type": "like"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cette offre n'est plus disponible."


def test_reaction_rejected_on_nonexistent_promotion(client):
    response = client.post(
        "/api/promotions/999999/reactions", json={"device_id": "device-1", "reaction_type": "like"}
    )
    assert response.status_code == 404


def test_promotion_mutations_require_admin(client):
    assert client.post("/api/promotions", json={"title": "x", "valid_until": "2030-01-01"}).status_code == 401
    assert client.get("/api/promotions/admin/all").status_code == 401


def test_search_filter_and_sort(client, admin_token):
    create_promotion(client, admin_token, title="Consultation pédiatrique", category="Pédiatrie")
    create_promotion(client, admin_token, title="Bilan cardiaque", category="Cardiologie")

    search_result = client.get("/api/promotions/all?search=cardiaque").json()
    assert all("cardiaque" in p["title"].lower() for p in search_result["items"])

    category_result = client.get("/api/promotions/all?category=Pédiatrie").json()
    assert all(p["category"] == "Pédiatrie" for p in category_result["items"])

    categories = client.get("/api/promotions/categories").json()
    assert "Pédiatrie" in categories and "Cardiologie" in categories
