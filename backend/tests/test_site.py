def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_public_can_send_message(client):
    response = client.post(
        "/api/messages",
        json={"name": "Konan Yves", "email": "k.yves@email.ci", "subject": "Prise de rendez-vous", "content": "Bonjour"},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "new"


def test_public_cannot_list_messages(client):
    response = client.get("/api/messages")
    assert response.status_code == 401


def test_admin_can_list_and_read_messages(client, admin_token):
    client.post("/api/messages", json={"name": "Adjoua Marie", "subject": "Info", "content": "Bonjour"})
    listing = client.get("/api/messages", headers=auth_headers(admin_token))
    assert listing.status_code == 200
    message_id = listing.json()[0]["id"]

    read = client.patch(f"/api/messages/{message_id}/read", headers=auth_headers(admin_token))
    assert read.status_code == 200
    assert read.json()["status"] == "read"
