from datetime import datetime

from app import create_app


def test_model_kendaraan_create_update_delete_flow():
    app = create_app()
    client = app.test_client()

    unique_suffix = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    created_id = None

    create_payload = {
        "id_merek": 1,
        "nama_model": f"Pytest Model {unique_suffix}",
    }

    try:
        create_response = client.post("/model-kendaraan", json=create_payload)
        assert create_response.status_code == 201

        create_json = create_response.get_json()
        assert create_json["success"] is True
        assert create_json["data"]["id_merek"] == 1
        assert create_json["data"]["nama_model"] == create_payload["nama_model"]

        created_id = create_json["data"]["id_model"]
        assert created_id is not None

        update_payload = {
            "nama_model": f"Pytest Model Updated {unique_suffix}",
        }
        update_response = client.put(
            f"/model-kendaraan/{created_id}",
            json=update_payload,
        )
        assert update_response.status_code == 200

        update_json = update_response.get_json()
        assert update_json["success"] is True
        assert update_json["data"]["id_model"] == created_id
        assert update_json["data"]["nama_model"] == update_payload["nama_model"]

        delete_response = client.delete(f"/model-kendaraan/{created_id}")
        assert delete_response.status_code == 200

        delete_json = delete_response.get_json()
        assert delete_json["success"] is True

    finally:
        if created_id is not None:
            client.delete(f"/model-kendaraan/{created_id}")
