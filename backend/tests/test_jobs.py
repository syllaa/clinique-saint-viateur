from datetime import date, timedelta


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def create_offer(client, admin_token, **overrides):
    payload = {"title": "Infirmier(ère) diplômé(e)", "contract_type": "CDI"}
    payload.update(overrides)
    return client.post("/api/jobs/offers", json=payload, headers=auth_headers(admin_token)).json()


def test_offer_crud_and_public_visibility(client, admin_token):
    offer = create_offer(client, admin_token)
    assert offer["slug"] == "infirmier-ere-diplome-e"

    public_list = client.get("/api/jobs/offers")
    assert any(o["id"] == offer["id"] for o in public_list.json())

    public_detail = client.get(f"/api/jobs/offers/{offer['slug']}")
    assert public_detail.status_code == 200

    update = client.patch(
        f"/api/jobs/offers/{offer['id']}", json={"department": "Soins"}, headers=auth_headers(admin_token)
    )
    assert update.json()["department"] == "Soins"

    delete = client.delete(f"/api/jobs/offers/{offer['id']}", headers=auth_headers(admin_token))
    assert delete.status_code == 204
    assert client.get(f"/api/jobs/offers/{offer['slug']}").status_code == 404


def test_offer_invalid_contract_type_rejected(client, admin_token):
    response = client.post(
        "/api/jobs/offers",
        json={"title": "Poste", "contract_type": "Bénévolat"},
        headers=auth_headers(admin_token),
    )
    assert response.status_code == 422


def test_draft_and_expired_offers_hidden_from_public(client, admin_token):
    draft = create_offer(client, admin_token, title="Poste brouillon", status="draft")
    expired = create_offer(
        client,
        admin_token,
        title="Poste expiré",
        application_deadline=(date.today() - timedelta(days=1)).isoformat(),
    )
    open_offer = create_offer(client, admin_token, title="Poste ouvert")

    public_slugs = {o["slug"] for o in client.get("/api/jobs/offers").json()}
    assert draft["slug"] not in public_slugs
    assert expired["slug"] not in public_slugs
    assert open_offer["slug"] in public_slugs

    assert client.get(f"/api/jobs/offers/{draft['slug']}").status_code == 404
    assert client.get(f"/api/jobs/offers/{expired['slug']}").status_code == 404

    admin_all = client.get("/api/jobs/offers/admin/all", headers=auth_headers(admin_token)).json()
    admin_slugs = {o["slug"] for o in admin_all}
    assert {draft["slug"], expired["slug"], open_offer["slug"]} <= admin_slugs


def _submit(client, slug, **overrides):
    data = {
        "first_name": "Awa",
        "last_name": "Traoré",
        "email": "awa.traore@email.ci",
        "phone": "+2250700000000",
        "cover_letter": "Motivée et disponible immédiatement.",
        "consent": "true",
    }
    data.update(overrides.pop("data", {}))
    files = overrides.pop("files", {"cv": ("cv.pdf", b"%PDF-1.4 fake pdf content", "application/pdf")})
    return client.post(f"/api/jobs/offers/{slug}/applications", data=data, files=files)


def test_application_submission_happy_path(client, admin_token):
    offer = create_offer(client, admin_token)
    response = _submit(client, offer["slug"])
    assert response.status_code == 201
    assert response.json()["status"] == "nouvelle"

    admin_list = client.get("/api/jobs/applications", headers=auth_headers(admin_token))
    assert len(admin_list.json()) == 1
    application_id = admin_list.json()[0]["id"]

    status_update = client.patch(
        f"/api/jobs/applications/{application_id}/status",
        json={"status": "en_cours"},
        headers=auth_headers(admin_token),
    )
    assert status_update.status_code == 200
    assert status_update.json()["status"] == "en_cours"


def test_application_rejects_missing_consent(client, admin_token):
    offer = create_offer(client, admin_token)
    response = _submit(client, offer["slug"], data={"consent": "false"})
    assert response.status_code == 422


def test_application_rejects_invalid_email(client, admin_token):
    offer = create_offer(client, admin_token)
    response = _submit(client, offer["slug"], data={"email": "not-an-email"})
    assert response.status_code == 422


def test_application_rejects_wrong_file_type(client, admin_token):
    offer = create_offer(client, admin_token)
    response = _submit(client, offer["slug"], files={"cv": ("cv.exe", b"MZ fake exe", "application/octet-stream")})
    assert response.status_code == 422


def test_application_rejects_expired_offer(client, admin_token):
    offer = create_offer(
        client, admin_token, application_deadline=(date.today() - timedelta(days=1)).isoformat()
    )
    response = _submit(client, offer["slug"])
    assert response.status_code == 404


def test_cv_download_requires_admin(client, admin_token):
    offer = create_offer(client, admin_token)
    application = _submit(client, offer["slug"]).json()

    unauthenticated = client.get(f"/api/jobs/applications/{application['id']}/cv")
    assert unauthenticated.status_code == 401

    authenticated = client.get(
        f"/api/jobs/applications/{application['id']}/cv", headers=auth_headers(admin_token)
    )
    assert authenticated.status_code == 200
    assert authenticated.content.startswith(b"%PDF")


def test_offer_mutations_require_admin(client):
    assert client.post("/api/jobs/offers", json={"title": "x", "contract_type": "CDI"}).status_code == 401
    assert client.get("/api/jobs/offers/admin/all").status_code == 401
    assert client.get("/api/jobs/applications").status_code == 401
