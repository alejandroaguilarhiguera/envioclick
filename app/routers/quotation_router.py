from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.schemas.schemas import QuotationRequest, Quotation, QuotationResponse
from app.services.quotation_service import QuotationService

router = APIRouter(prefix="/quotation", tags=["Quotations"])


@router.post(
    "/",
    response_model=QuotationResponse,
    status_code=status.HTTP_200_OK
)
def get_all(
    quotation_in: QuotationRequest,
    service: QuotationService = Depends(QuotationService),
):
   return service.get_quotation(quotation_in)
    # return service.get_quotation()
