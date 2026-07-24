def test_create_asset(client, auth_headers):
    response = client.post(
        "/assets/",
        headers=auth_headers,
        json={
            "serial_number": "DRN001",
            "asset_type": "DRONE",
            "status": "ONLINE",
            "name": "Drone A",
            "description": "Survey Drone",
            "latitude": 12.2958,
            "longitude": 76.6394,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["serial_number"] == "DRN001"
    assert data["asset_type"] == "DRONE"
    assert data["status"] == "ONLINE"
    assert data["name"] == "Drone A"
    assert data["description"] == "Survey Drone"
    assert data["latitude"] == 12.2958
    assert data["longitude"] == 76.6394
    assert "id" in data


def test_get_all_assets(client, auth_headers):
    client.post(
        "/assets/",
        headers=auth_headers,
        json={
            "serial_number": "DRN001",
            "asset_type": "DRONE",
            "status": "ONLINE",
            "name": "Drone A",
            "description": "Survey Drone",
            "latitude": 12.2958,
            "longitude": 76.6394,
        },
    )

    response = client.get(
        "/assets/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1

    asset = data["items"][0]

    assert asset["serial_number"] == "DRN001"
    assert asset["asset_type"] == "DRONE"
    assert asset["status"] == "ONLINE"
    assert asset["name"] == "Drone A"


def test_get_asset_by_id(client, auth_headers):
    create = client.post(
        "/assets/",
        headers=auth_headers,
        json={
            "serial_number": "DRN001",
            "asset_type": "DRONE",
            "status": "ONLINE",
            "name": "Drone A",
            "description": "Survey Drone",
            "latitude": 12.2958,
            "longitude": 76.6394,
        },
    )

    assert create.status_code == 201

    asset_id = create.json()["id"]

    response = client.get(
        f"/assets/{asset_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == asset_id
    assert data["serial_number"] == "DRN001"
    assert data["asset_type"] == "DRONE"
    assert data["status"] == "ONLINE"
    assert data["name"] == "Drone A"


def test_asset_not_found(client, auth_headers):
    response = client.get(
        "/assets/99999",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Asset not found."


def test_update_asset(client, auth_headers):
    create = client.post(
        "/assets/",
        headers=auth_headers,
        json={
            "serial_number": "DRN001",
            "asset_type": "DRONE",
            "status": "ONLINE",
            "name": "Drone A",
            "description": "Survey Drone",
            "latitude": 12.2958,
            "longitude": 76.6394,
        },
    )

    assert create.status_code == 201

    asset_id = create.json()["id"]

    response = client.put(
        f"/assets/{asset_id}",
        headers=auth_headers,
        json={
            "serial_number": "DRN002",
            "asset_type": "DRONE",
            "status": "OFFLINE",
            "name": "Updated Drone",
            "description": "Updated Description",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["serial_number"] == "DRN002"
    assert data["asset_type"] == "DRONE"
    assert data["status"] == "OFFLINE"
    assert data["name"] == "Updated Drone"
    assert data["description"] == "Updated Description"
    assert data["latitude"] == 12.2958
    assert data["longitude"] == 76.6394


def test_delete_asset(client, auth_headers):
    create = client.post(
        "/assets/",
        headers=auth_headers,
        json={
            "serial_number": "DRN001",
            "asset_type": "DRONE",
            "status": "ONLINE",
            "name": "Drone A",
            "description": "Survey Drone",
            "latitude": 12.2958,
            "longitude": 76.6394,
        },
    )

    assert create.status_code == 201

    asset_id = create.json()["id"]

    response = client.delete(
        f"/assets/{asset_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Asset deleted successfully."

    response = client.get(
        f"/assets/{asset_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_update_asset_not_found(client, auth_headers):
    response = client.put(
        "/assets/99999",
        headers=auth_headers,
        json={
            "name": "New Name",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Asset not found."


def test_delete_asset_not_found(client, auth_headers):
    response = client.delete(
        "/assets/99999",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Asset not found."