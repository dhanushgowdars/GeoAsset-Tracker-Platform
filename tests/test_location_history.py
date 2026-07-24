def create_asset(
    client,
    auth_headers,
    serial_number,
    name,
    latitude=12.2958,
    longitude=76.6394,
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
            "latitude": latitude,
            "longitude": longitude,
        },
    )

    assert response.status_code == 201
    return response.json()


def test_location_history_requires_authentication(client):
    response = client.get("/location-history/1")

    assert response.status_code in (401, 403)


def test_empty_location_history(client, auth_headers):
    asset = create_asset(
        client,
        auth_headers,
        "DRN001",
        "Drone A",
    )

    response = client.get(
        f"/location-history/{asset['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "history" in data
    assert data["history"] == []


def test_location_history_after_updates(client, auth_headers):
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
            "latitude": 13.0,
            "longitude": 77.0,
        },
    )

    assert response.status_code == 200

    response = client.put(
        f"/assets/{asset['id']}",
        headers=auth_headers,
        json={
            "latitude": 14.0,
            "longitude": 78.0,
        },
    )

    assert response.status_code == 200

    response = client.get(
        f"/location-history/{asset['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    history = response.json()["history"]

    assert len(history) == 2

    latitudes = {record["latitude"] for record in history}
    longitudes = {record["longitude"] for record in history}

    assert latitudes == {13.0, 14.0}
    assert longitudes == {77.0, 78.0}


def test_location_history_invalid_asset(client, auth_headers):
    response = client.get(
        "/location-history/999999",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["history"] == []


def test_location_history_records_are_complete(client, auth_headers):
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
            "latitude": 13.0,
            "longitude": 77.0,
        },
    )

    assert response.status_code == 200

    response = client.get(
        f"/location-history/{asset['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    history = response.json()["history"]

    assert len(history) == 1

    record = history[0]

    assert "id" in record
    assert "asset_id" in record
    assert "latitude" in record
    assert "longitude" in record
    assert "recorded_at" in record