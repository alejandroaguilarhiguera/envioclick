# tests/test_health.py
import pytest

mock_request = {
    "origin_address": "Av. Revolución",
    "origin_number": "381",
    "origin_zip_code": "44100",
    "origin_suburb": "Guadalajara Centro",
    "destination_address": "Calzada Lázaro Cárdenas",
    "destination_number": "624",
    "destination_zip_code": "44200",
    "destination_suburb": "El Santuario",
    "package": {
        "description": "Pink iPad",
        "contentValue": 120.01,
        "weight": 1.01,
        "length": 30.01,
        "height": 15.01,
        "width": 20.01
    }
}

@pytest.mark.anyio
async def test_quotation_check(client):
    response = await client.post("/quotation/", json=mock_request)
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert data["status"] == "OK"
    assert data["status_codes"] == [200]
    
    response_data = data["data"]
    assert response_data["originZipCode"] == mock_request["origin_zip_code"]
    assert response_data["destinationZipCode"] == mock_request["destination_zip_code"]

    for rate in response_data["rates"]:
        assert "idRate" in rate
        assert isinstance(rate["idRate"], int)
        
        assert "carrier" in rate
        assert isinstance(rate["carrier"], str)
        
        assert "total" in rate
        assert isinstance(rate["total"], (int, float))
        assert rate["total"] > 0
        
        assert "deliveryDays" in rate
        assert isinstance(rate["deliveryDays"], int)

    assert response_data["package"]["weight"] == mock_request["package"]["weight"]
    assert response_data["package"]["length"] == mock_request["package"]["length"]