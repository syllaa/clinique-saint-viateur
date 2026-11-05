def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_ticket_requires_admin(client):
    response = client.get("/api/support/tickets")
    assert response.status_code == 401


def test_create_and_list_ticket(client, admin_token):
    create = client.post(
        "/api/support/tickets",
        json={"subject": "Panne du portail patient", "description": "Le portail ne se charge plus.", "priority": "high"},
        headers=auth_headers(admin_token),
    )
    assert create.status_code == 201
    ticket_id = create.json()["id"]

    listing = client.get("/api/support/tickets", headers=auth_headers(admin_token))
    assert listing.status_code == 200
    assert any(t["id"] == ticket_id for t in listing.json())


def test_update_ticket_status(client, admin_token):
    create = client.post(
        "/api/support/tickets",
        json={"subject": "Test", "description": "desc"},
        headers=auth_headers(admin_token),
    )
    ticket_id = create.json()["id"]

    update = client.patch(
        f"/api/support/tickets/{ticket_id}",
        json={"status": "closed"},
        headers=auth_headers(admin_token),
    )
    assert update.status_code == 200
    assert update.json()["status"] == "closed"


def test_invalid_status_rejected(client, admin_token):
    create = client.post(
        "/api/support/tickets",
        json={"subject": "Test", "description": "desc"},
        headers=auth_headers(admin_token),
    )
    ticket_id = create.json()["id"]

    update = client.patch(
        f"/api/support/tickets/{ticket_id}",
        json={"status": "bogus"},
        headers=auth_headers(admin_token),
    )
    assert update.status_code == 422
