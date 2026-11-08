# tests/test_all.py
import pytest

@pytest.fixture
def mock_request():
    return {
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

@pytest.fixture
async def quotation_data(client, mock_request):
    response = await client.post("/quotation/", json=mock_request)
    assert response.status_code == 200
    return response.json()["data"]

@pytest.fixture
async def shipment_data(client, quotation_data, mock_request):
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
            "email": "alejandro.aguilar@example.com",
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
    return response.json()["data"]


@pytest.mark.anyio
async def test_quotation_check(quotation_data, mock_request):
    assert quotation_data["originZipCode"] == mock_request["origin_zip_code"]
    assert quotation_data["destinationZipCode"] == mock_request["destination_zip_code"]


@pytest.mark.anyio
async def test_shipment(shipment_data, mock_request):
    assert isinstance(shipment_data["guide"], str)
    assert len(shipment_data["guide"]) > 0
    assert shipment_data["origin"]["zipCode"] == mock_request["origin_zip_code"]

@pytest.mark.anyio
async def test_track_single(client, shipment_data):
    """POST 'track/' con un único tracking code"""
    tracking_code = shipment_data.get("tracker")
    
    response = await client.post("/track", json={"trackingCode": tracking_code})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert data["status_codes"] == [200]
    track_info = data["data"]

    assert "status" in track_info
    assert isinstance(track_info["status"], str)
    
    assert "statusDetail" in track_info
    assert isinstance(track_info["statusDetail"], str)
    
    assert "arrivalDate" in track_info
    assert "realPickupDate" in track_info
    assert "realDeliveryDate" in track_info
    assert "receivedBy" in track_info


@pytest.mark.anyio
async def test_track_by_order_get(client, shipment_data):
    """GET 'track-by-orders/{idOrder}'"""
    order_id = shipment_data.get("idOrder")
    
    response = await client.get(f"/track-by-orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert data["status_codes"] == [200]
    track_info = data["data"]

    assert "status" in track_info
    assert isinstance(track_info["status"], str)
    
    assert "statusDetail" in track_info
    assert isinstance(track_info["statusDetail"], str)
    
    assert "arrivalDate" in track_info
    assert "realPickupDate" in track_info
    assert "realDeliveryDate" in track_info
    assert "receivedBy" in track_info


@pytest.mark.anyio
async def test_track_batch(client, shipment_data):
    """POST 'track-batch/' con una lista de tracking codes"""
    tracking_code = shipment_data.get("tracker")
    
    response = await client.post("/track-batch", json={"trackingCodes": [tracking_code]})
    assert response.status_code == 200
    
    data = response.json()
    
    assert data["status"] == "OK"
    assert data["status_codes"] == [200]
    
    track_results = data["data"]
    
    assert tracking_code in track_results
    valid_tracking_info = track_results[tracking_code]
    
    assert isinstance(valid_tracking_info, dict)
    assert "status" in valid_tracking_info
    assert "statusDetail" in valid_tracking_info

@pytest.mark.anyio
async def test_track_by_orders_post(client, shipment_data):
    """POST 'track-by-orders' con un arreglo de órdenes"""
    order_id = shipment_data.get("idOrder")
    
    response = await client.post("/track-by-orders", json={"orders": [order_id]})
    assert response.status_code == 200
    
    data = response.json()
    
    assert data["status"] == "OK"
    assert data["status_codes"] == [200]
    assert data["status_messages"][0]["request"] == "Request processed."
    
    track_results = data["data"]
    
    str_order_id = str(order_id)
    assert str_order_id in track_results
    
    order_info = track_results[str_order_id]
    
    assert isinstance(order_info, dict)
    assert "status" in order_info
    assert isinstance(order_info["status"], str)
    
    assert "statusDetail" in order_info
    assert "arrivalDate" in order_info
    assert "realPickupDate" in order_info
    assert "realDeliveryDate" in order_info
    assert "receivedBy" in order_info