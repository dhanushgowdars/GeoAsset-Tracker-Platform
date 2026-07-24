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


def test_dashboard_requires_authentication(client):
    response = client.get("/dashboard/summary")

    assert response.status_code in (401, 403)


def test_empty_dashboard(client, auth_headers):
    response = client.get(
        "/dashboard/summary",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status_summary"]["total_assets"] == 0
    assert data["status_summary"]["online_assets"] == 0
    assert data["status_summary"]["offline_assets"] == 0
    assert data["status_summary"]["maintenance_assets"] == 0
    assert data["status_summary"]["retired_assets"] == 0

    assert data["asset_type_summary"] == []


def test_dashboard_single_asset(client, auth_headers):
    create_asset(
        client,
        auth_headers,
        serial_number="DRN001",
        name="Drone A",
    )

    response = client.get(
        "/dashboard/summary",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status_summary"]["total_assets"] == 1
    assert data["status_summary"]["online_assets"] == 1
    assert data["status_summary"]["offline_assets"] == 0
    assert data["status_summary"]["maintenance_assets"] == 0
    assert data["status_summary"]["retired_assets"] == 0

    asset_types = {
        item["asset_type"]: item["count"]
        for item in data["asset_type_summary"]
    }

    assert asset_types["DRONE"] == 1


def test_dashboard_multiple_statuses(client, auth_headers):
    create_asset(
        client,
        auth_headers,
        "DRN001",
        "Drone A",
        status="ONLINE",
    )

    create_asset(
        client,
        auth_headers,
        "VEH001",
        "Vehicle A",
        asset_type="VEHICLE",
        status="OFFLINE",
    )

    create_asset(
        client,
        auth_headers,
        "CAM001",
        "Camera A",
        asset_type="CAMERA",
        status="MAINTENANCE",
    )

    create_asset(
        client,
        auth_headers,
        "SEN001",
        "Sensor A",
        asset_type="SENSOR",
        status="RETIRED",
    )

    response = client.get(
        "/dashboard/summary",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    summary = data["status_summary"]

    assert summary["total_assets"] == 4
    assert summary["online_assets"] == 1
    assert summary["offline_assets"] == 1
    assert summary["maintenance_assets"] == 1
    assert summary["retired_assets"] == 1

    asset_types = {
        item["asset_type"]: item["count"]
        for item in data["asset_type_summary"]
    }

    assert asset_types["DRONE"] == 1
    assert asset_types["VEHICLE"] == 1
    assert asset_types["CAMERA"] == 1
    assert asset_types["SENSOR"] == 1


def test_dashboard_excludes_deleted_assets(client, auth_headers):
    asset = create_asset(
        client,
        auth_headers,
        "DRN001",
        "Drone A",
    )

    client.delete(
        f"/assets/{asset['id']}",
        headers=auth_headers,
    )

    response = client.get(
        "/dashboard/summary",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    summary = data["status_summary"]

    assert summary["total_assets"] == 0
    assert summary["online_assets"] == 0
    assert summary["offline_assets"] == 0
    assert summary["maintenance_assets"] == 0
    assert summary["retired_assets"] == 0

    assert data["asset_type_summary"] == []