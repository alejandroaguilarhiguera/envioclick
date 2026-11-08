from fastapi import APIRouter, Depends, status

from app.schemas.schemas import ShipmentRequest, ShipmentResponse
from app.services.shipment_service import ShipmentService

router = APIRouter(
    prefix="/shipment",
    tags=["Shipments"]
)


@router.post(
    "/",
    response_model=ShipmentResponse,
    status_code=status.HTTP_200_OK,
)
def create_shipment(
    shipment_in: ShipmentRequest,
    service: ShipmentService = Depends(ShipmentService),
):
    return service.create_shipment(shipment_in)