from fastapi import APIRouter, Depends, status

from app.schemas.schemas import (
    CancellationRequest,
    CancellationResponse
)

from app.services.cancellation_service import CancellationService


router = APIRouter(
    prefix="/cancellation",
    tags=["Cancellations"]
)


@router.post(
    "/batch/order",
    response_model=CancellationResponse,
    status_code=status.HTTP_200_OK
)
def cancel_shipments(
    cancellation_in: CancellationRequest,
    service: CancellationService = Depends(CancellationService),
):
    return service.cancel_shipments(cancellation_in.idOrders)