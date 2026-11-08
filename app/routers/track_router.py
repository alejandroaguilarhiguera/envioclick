from fastapi import APIRouter, Depends, status

from app.schemas.schemas import TrackResponse, TrackingCodeRequest, TrackBatchResponse, TrackingCodesRequest, TrackOrdersRequest
from app.services.track_service import TrackService

router = APIRouter(
    tags=["Track"]
)

@router.get(
    "/track-by-orders/{track_id}",
    response_model=TrackResponse,
    status_code=status.HTTP_200_OK,
)
def get_track_by_orders(
    track_id: str,
    service: TrackService = Depends(TrackService),
):
    return service.get_by_id(track_id)

@router.post(
    "/track",
    response_model=TrackResponse,
    status_code=status.HTTP_200_OK,
)
def get_track(
    trackingCodeRequest: TrackingCodeRequest,
    service: TrackService = Depends(TrackService),
):
    return service.get_by_request(trackingCodeRequest.trackingCode)

@router.post(
    "/track-batch",
    response_model=TrackBatchResponse,
    status_code=status.HTTP_200_OK,
)
def get_track_batch(
    trackingCodesRequest: TrackingCodesRequest,
    service: TrackService = Depends(TrackService),
):
    return service.get_tracking_codes(trackingCodesRequest.trackingCodes)

@router.post(
    "/track-by-orders",
    response_model=TrackBatchResponse,
    status_code=status.HTTP_200_OK,
)
def get_track_batch(
    ordersRequest: TrackOrdersRequest,
    service: TrackService = Depends(TrackService),
):
    return service.get_by_orders(ordersRequest.orders)
