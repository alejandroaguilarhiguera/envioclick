# tests/test_shipment.py
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
async def test_shipment_check(client):
    quotation_response = await client.post("/quotation/", json=mock_request)
    assert quotation_response.status_code == 200

    quotation_data = quotation_response.json()["data"]
    rates = quotation_data["rates"]
    assert len(rates) > 0
    selected_rate = rates[0]
    
    shipment_payload = {
        "idRate": selected_rate["idRate"],
        "myShipmentReference": "My Shipment 1A",
        "requestPickup": True,
        "pickupDate": "2027-01-20",
        "insurance": True,
        "countryCode": "MX",
        "package": {
            **mock_request["package"],
            "items": [
                {
                    "weight_unit_key": "XPK",
                    "product_key": "31181701",
                    "is_dangerous": 0,
                    "c_TipoEmbalaje": None,
                    "contentValue": 100.5,
                    "units": 1,
                    "c_ClaveUnidadPeso": "KGM",
                    "c_ClaveProdServCP": "31181701"
                }
            ]
        },
        "origin": {
            "company": "Mi Empresa",
            "rfc": "XAXX010101000",
            "firstName": "Alejandro",
            "lastName": "Aguilar",
            "email": "alejandro.aguilar@gmail.com",
            "phone": "3333333333",
            "street": mock_request["origin_address"],
            "number": mock_request["origin_number"],
            "intNumber": "1",
            "suburb": mock_request["origin_suburb"],
            "crossStreet": "Calle principal",
            "zipCode": mock_request["origin_zip_code"],
            "reference": "Puerta principal",
            "observations": "Recolección en planta baja"
        },
        "destination": {
            "company": "Cliente Destino",
            "rfc": "XAXX010101000",
            "firstName": "Pedro",
            "lastName": "López",
            "email": "pedro.lopez@example.com",
            "phone": "3333333333",
            "street": mock_request["destination_address"],
            "number": mock_request["destination_number"],
            "intNumber": "",
            "suburb": mock_request["destination_suburb"],
            "crossStreet": "",
            "zipCode": mock_request["destination_zip_code"],
            "reference": "Ventana blanca",
            "observations": "Entregar en recepción"
        }
    }
    
    response = await client.post("/shipment/", json=shipment_payload)
    assert response.status_code == 200
    
    data = response.json()
    
    assert data["status"] == "OK"
    assert data["status_codes"] == [200]
    
    shipment = data["data"]
    
    assert shipment["idRate"] == selected_rate["idRate"]
    assert isinstance(shipment["guide"], str)
    assert len(shipment["guide"]) > 0
    
    assert shipment["origin"]["zipCode"] == mock_request["origin_zip_code"]
    assert shipment["destination"]["zipCode"] == mock_request["destination_zip_code"]

    assert shipment["package"]["weight"] == mock_request["package"]["weight"]