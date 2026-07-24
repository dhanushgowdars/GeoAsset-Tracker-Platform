def create_asset(
    client,
    auth_headers,
    serial_number,
    name,
):
    response = client.post(
        "/assets/",
        headers=auth_headers,
        json={
            "serial_number": serial_number,
            "asset_type": "DRONE",
            "status": "ONLINE",
            "name": name,
            "description": "Test Asset",
            "latitude": 12.2958,
            "longitude": 76.6394,
        },
    )

    assert response.status_code == 201
    return response.json()


def test_get_empty_audit_logs(client):
    response = client.get("/audit-logs/")

    assert response.status_code == 200
    assert response.json() == []


def test_asset_creation_creates_audit_log(client, auth_headers):
    asset = create_asset(
        client,
        auth_headers,
        "DRN001",
        "Drone A",
    )

    response = client.get("/audit-logs/")

    assert response.status_code == 200

    logs = response.json()

    assert len(logs) >= 1

    latest = logs[0]

    assert latest["entity"] == "Asset"
    assert latest["entity_id"] == asset["id"]
    assert latest["action"] == "CREATE"


def test_asset_update_creates_audit_log(client, auth_headers):
    asset = create_asset(
        client,
        auth_headers,
        "DRN001",
        "Drone A",
    )

    response = client.put(
        f"/assets/{asset['id']}",
        headers=auth_headers,
        json={
            "name": "Updated Drone",
        },
    )

    assert response.status_code == 200

    logs = client.get("/audit-logs/").json()

    update_logs = [
        log
        for log in logs
        if log["action"] == "UPDATE"
        and log["entity_id"] == asset["id"]
    ]

    assert len(update_logs) == 1


def test_asset_delete_creates_audit_log(client, auth_headers):
    asset = create_asset(
        client,
        auth_headers,
        "DRN001",
        "Drone A",
    )

    response = client.delete(
        f"/assets/{asset['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    logs = client.get("/audit-logs/").json()

    delete_logs = [
        log
        for log in logs
        if log["action"] == "DELETE"
        and log["entity_id"] == asset["id"]
    ]

    assert len(delete_logs) == 1
