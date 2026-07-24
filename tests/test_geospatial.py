def create_test_asset(client, auth_headers, name, latitude, longitude):
    response = client.post(
        "/assets/",
        headers=auth_headers,
        json={
            "serial_number": "DRN001",
            "asset_type": "DRONE",
            "status": "ONLINE",
            "name": name,
            "description": f"{name} Description",
            "latitude": latitude,
            "longitude": longitude,
         }
    )

    assert response.status_code == 201
    return response.json()


def test_nearby_assets(client, auth_headers):
    create_test_asset(
        client,
        auth_headers,
        "Drone A",
        12.2958,
        76.6394,
    )

    response = client.get(
        "/assets/nearby",
        headers=auth_headers,
        params={
            "latitude": 12.2958,
            "longitude": 76.6394,
            "radius_km": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[0]["name"] == "Drone A"
    assert "distance_km" in data[0]


def test_nearest_asset(client, auth_headers):
    create_test_asset(
        client,
        auth_headers,
        "Nearest Drone",
        12.2958,
        76.6394,
    )

    response = client.get(
        "/assets/nearest",
        headers=auth_headers,
        params={
            "latitude": 12.2958,
            "longitude": 76.6394,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Nearest Drone"
    assert "distance_km" in data


def test_distance_to_asset(client, auth_headers):
    asset = create_test_asset(
        client,
        auth_headers,
        "Distance Drone",
        12.2958,
        76.6394,
    )

    response = client.get(
        f"/assets/{asset['id']}/distance",
        headers=auth_headers,
        params={
            "latitude": 12.3000,
            "longitude": 76.6400,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["asset_id"] == asset["id"]
    assert data["distance_km"] >= 0


def test_assets_in_bounding_box(client, auth_headers):
    create_test_asset(
        client,
        auth_headers,
        "Bounding Drone",
        12.2958,
        76.6394,
    )

    response = client.get(
        "/assets/bbox",
        headers=auth_headers,
        params={
            "min_latitude": 12.2900,
            "min_longitude": 76.6300,
            "max_latitude": 12.3000,
            "max_longitude": 76.6500,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Bounding Drone"


def test_empty_bounding_box(client, auth_headers):
    response = client.get(
        "/assets/bbox",
        headers=auth_headers,
        params={
            "min_latitude": 0,
            "min_longitude": 0,
            "max_latitude": 1,
            "max_longitude": 1,
        },
    )

    assert response.status_code == 200
    assert response.json() == []


def test_geofence(client, auth_headers):
    create_test_asset(
        client,
        auth_headers,
        "Geofence Drone",
        12.2958,
        76.6394,
    )

    response = client.post(
        "/assets/geofence",
        headers=auth_headers,
        json={
            "coordinates": [
                [76.6300, 12.2900],
                [76.6500, 12.2900],
                [76.6500, 12.3000],
                [76.6300, 12.3000],
            ]
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Geofence Drone"


def test_invalid_geofence(client, auth_headers):
    response = client.post(
        "/assets/geofence",
        headers=auth_headers,
        json={
            "coordinates": [
                [76.6300, 12.2900],
                [76.6500, 12.2900],
            ]
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "A polygon must contain at least three points."


def test_invalid_radius(client, auth_headers):
    response = client.get(
        "/assets/nearby",
        headers=auth_headers,
        params={
            "latitude": 12.2958,
            "longitude": 76.6394,
            "radius_km": -5,
        },
    )

    assert response.status_code in (400, 422)
