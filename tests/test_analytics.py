def create_asset(
    client,
    auth_headers,
    serial_number,
    name,
    asset_type="DRONE",
    status="ONLINE",
):
    response = client.post(
        "/assets/",
        headers=auth_headers,
        json={
            "serial_number": serial_number,
            "asset_type": asset_type,
            "status": status,
            "name": name,
            "description": f"{name} Description",
            "latitude": 12.2958,
            "longitude": 76.6394,
        },
    )

    assert response.status_code == 201
    return response.json()


def test_analytics_requires_authentication(client):
    response = client.get("/analytics/summary")

    assert response.status_code in (401, 403)


def test_empty_analytics(client, auth_headers):
    response = client.get(
        "/analytics/summary",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_assets"] == 0
    assert data["online_assets"] == 0
    assert data["offline_assets"] == 0
    assert data["maintenance_assets"] == 0
    assert data["retired_assets"] == 0

    assert data["assets_by_type"]["DRONE"] == 0
    assert data["assets_by_type"]["VEHICLE"] == 0
    assert data["assets_by_type"]["CAMERA"] == 0
    assert data["assets_by_type"]["SENSOR"] == 0
    assert data["assets_by_type"]["INFRASTRUCTURE"] == 0
    assert data["assets_by_type"]["OTHER"] == 0


def test_single_asset_analytics(client, auth_headers):
    create_asset(
        client,
        auth_headers,
        "DRN001",
        "Drone A",
    )

    response = client.get(
        "/analytics/summary",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_assets"] == 1
    assert data["online_assets"] == 1
    assert data["offline_assets"] == 0
    assert data["maintenance_assets"] == 0
    assert data["retired_assets"] == 0

    assert data["assets_by_type"]["DRONE"] == 1


def test_multiple_asset_types_and_statuses(client, auth_headers):
    create_asset(
        client,
        auth_headers,
        "DRN001",
        "Drone",
        asset_type="DRONE",
        status="ONLINE",
    )

    create_asset(
        client,
        auth_headers,
        "VEH001",
        "Vehicle",
        asset_type="VEHICLE",
        status="OFFLINE",
    )

    create_asset(
        client,
        auth_headers,
        "CAM001",
        "Camera",
        asset_type="CAMERA",
        status="MAINTENANCE",
    )

    create_asset(
        client,
        auth_headers,
        "SEN001",
        "Sensor",
        asset_type="SENSOR",
        status="RETIRED",
    )

    response = client.get(
        "/analytics/summary",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_assets"] == 4
    assert data["online_assets"] == 1
    assert data["offline_assets"] == 1
    assert data["maintenance_assets"] == 1
    assert data["retired_assets"] == 1

    assert data["assets_by_type"]["DRONE"] == 1
    assert data["assets_by_type"]["VEHICLE"] == 1
    assert data["assets_by_type"]["CAMERA"] == 1
    assert data["assets_by_type"]["SENSOR"] == 1
    assert data["assets_by_type"]["INFRASTRUCTURE"] == 0
    assert data["assets_by_type"]["OTHER"] == 0


def test_deleted_assets_not_counted(client, auth_headers):
    asset = create_asset(
        client,
        auth_headers,
        "DRN001",
        "Drone",
    )

    response = client.delete(
        f"/assets/{asset['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    response = client.get(
        "/analytics/summary",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_assets"] == 0
    assert data["online_assets"] == 0
    assert data["assets_by_type"]["DRONE"] == 0