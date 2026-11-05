def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_specialty_crud_and_public_visibility(client, admin_token):
    create = client.post(
        "/api/specialties",
        json={"name": "Cardiologie", "description": "Diagnostic et suivi", "icon_name": "heart-pulse"},
        headers=auth_headers(admin_token),
    )
    assert create.status_code == 201
    specialty = create.json()
    assert specialty["slug"] == "cardiologie"
    assert specialty["media_type"] == "icon"
    assert specialty["icon_name"] == "heart-pulse"
    specialty_id = specialty["id"]

    public_list = client.get("/api/specialties")
    assert any(s["id"] == specialty_id for s in public_list.json())

    public_detail = client.get(f"/api/specialties/{specialty['slug']}")
    assert public_detail.status_code == 200
    assert public_detail.json()["name"] == "Cardiologie"

    update = client.patch(
        f"/api/specialties/{specialty_id}",
        json={"full_description": "Prise en charge complète des maladies cardiovasculaires."},
        headers=auth_headers(admin_token),
    )
    assert update.status_code == 200
    assert update.json()["full_description"].startswith("Prise en charge")

    delete = client.delete(f"/api/specialties/{specialty_id}", headers=auth_headers(admin_token))
    assert delete.status_code == 204
    assert client.get(f"/api/specialties/{specialty['slug']}").status_code == 404


def test_specialty_toggle_active_hides_from_public(client, admin_token):
    create = client.post(
        "/api/specialties",
        json={"name": "Neurologie"},
        headers=auth_headers(admin_token),
    )
    specialty = create.json()

    toggled = client.patch(
        f"/api/specialties/{specialty['id']}/toggle-active", headers=auth_headers(admin_token)
    )
    assert toggled.status_code == 200
    assert toggled.json()["is_active"] is False

    assert client.get(f"/api/specialties/{specialty['slug']}").status_code == 404
    assert all(s["id"] != specialty["id"] for s in client.get("/api/specialties").json())

    admin_list = client.get("/api/specialties/admin/all", headers=auth_headers(admin_token))
    assert any(s["id"] == specialty["id"] for s in admin_list.json())


def test_specialty_slug_collision_is_disambiguated(client, admin_token):
    first = client.post("/api/specialties", json={"name": "Pédiatrie"}, headers=auth_headers(admin_token))
    second = client.post("/api/specialties", json={"name": "Pédiatrie"}, headers=auth_headers(admin_token))
    assert first.json()["slug"] == "pediatrie"
    assert second.json()["slug"] == "pediatrie-2"


def test_specialty_doctors_and_faqs_crud(client, admin_token):
    specialty = client.post(
        "/api/specialties", json={"name": "Gynécologie"}, headers=auth_headers(admin_token)
    ).json()

    doctor = client.post(
        f"/api/specialties/{specialty['id']}/doctors",
        json={"name": "Dr. Koffi", "title": "Gynécologue"},
        headers=auth_headers(admin_token),
    )
    assert doctor.status_code == 201
    doctor_id = doctor.json()["id"]

    faq = client.post(
        f"/api/specialties/{specialty['id']}/faqs",
        json={"question": "Faut-il un rendez-vous ?", "answer": "Oui, de préférence."},
        headers=auth_headers(admin_token),
    )
    assert faq.status_code == 201
    faq_id = faq.json()["id"]

    detail = client.get(f"/api/specialties/{specialty['slug']}").json()
    assert detail["doctors"][0]["name"] == "Dr. Koffi"
    assert detail["faqs"][0]["question"] == "Faut-il un rendez-vous ?"

    client.patch(
        f"/api/specialties/doctors/{doctor_id}", json={"title": "Chef de service"}, headers=auth_headers(admin_token)
    )
    updated_detail = client.get(f"/api/specialties/{specialty['slug']}").json()
    assert updated_detail["doctors"][0]["title"] == "Chef de service"

    assert client.delete(f"/api/specialties/doctors/{doctor_id}", headers=auth_headers(admin_token)).status_code == 204
    assert client.delete(f"/api/specialties/faqs/{faq_id}", headers=auth_headers(admin_token)).status_code == 204

    final_detail = client.get(f"/api/specialties/{specialty['slug']}").json()
    assert final_detail["doctors"] == []
    assert final_detail["faqs"] == []


def test_specialty_deletion_cascades_children(client, admin_token):
    specialty = client.post(
        "/api/specialties", json={"name": "Dermatologie"}, headers=auth_headers(admin_token)
    ).json()
    client.post(
        f"/api/specialties/{specialty['id']}/doctors",
        json={"name": "Dr. Bamba"},
        headers=auth_headers(admin_token),
    )

    delete = client.delete(f"/api/specialties/{specialty['id']}", headers=auth_headers(admin_token))
    assert delete.status_code == 204
    assert client.get(f"/api/specialties/{specialty['slug']}").status_code == 404


def test_specialty_mutations_require_admin(client):
    assert client.post("/api/specialties", json={"name": "X"}).status_code == 401
    assert client.get("/api/specialties/admin/all").status_code == 401


def test_specialty_defaults_to_icon_with_fallback_name(client, admin_token):
    """Creating without specifying an icon_name must still yield a valid, non-null
    icon so the frontend never has to special-case a missing icon (§11.9)."""
    created = client.post(
        "/api/specialties", json={"name": "Endocrinologie"}, headers=auth_headers(admin_token)
    ).json()
    assert created["media_type"] == "icon"
    assert created["icon_name"] == "hospital"


def test_specialty_image_media_type_requires_image(client, admin_token):
    response = client.post(
        "/api/specialties",
        json={"name": "Rhumatologie", "media_type": "image"},
        headers=auth_headers(admin_token),
    )
    assert response.status_code == 422


def test_specialty_image_media_type_accepted_with_image(client, admin_token):
    created = client.post(
        "/api/specialties",
        json={
            "name": "Rhumatologie",
            "media_type": "image",
            "cover_image_url": "/uploads/images/fake.webp",
            "image_alt": "Salle de consultation en rhumatologie",
        },
        headers=auth_headers(admin_token),
    ).json()
    assert created["media_type"] == "image"
    assert created["cover_image_url"] == "/uploads/images/fake.webp"
    assert created["image_alt"] == "Salle de consultation en rhumatologie"
    assert created["icon_name"] is None


def test_specialty_switch_from_image_to_icon_via_update(client, admin_token):
    specialty = client.post(
        "/api/specialties",
        json={"name": "Allergologie", "media_type": "image", "cover_image_url": "/uploads/images/x.webp"},
        headers=auth_headers(admin_token),
    ).json()

    switched = client.patch(
        f"/api/specialties/{specialty['id']}",
        json={"media_type": "icon", "icon_name": "stethoscope"},
        headers=auth_headers(admin_token),
    )
    assert switched.status_code == 200
    assert switched.json()["media_type"] == "icon"
    assert switched.json()["icon_name"] == "stethoscope"


def test_specialty_update_to_image_without_existing_image_rejected(client, admin_token):
    specialty = client.post(
        "/api/specialties", json={"name": "Urologie", "icon_name": "stethoscope"}, headers=auth_headers(admin_token)
    ).json()

    response = client.patch(
        f"/api/specialties/{specialty['id']}", json={"media_type": "image"}, headers=auth_headers(admin_token)
    )
    assert response.status_code == 422


def test_specialty_invalid_media_type_rejected(client, admin_token):
    response = client.post(
        "/api/specialties",
        json={"name": "Angiologie", "media_type": "video"},
        headers=auth_headers(admin_token),
    )
    assert response.status_code == 422
