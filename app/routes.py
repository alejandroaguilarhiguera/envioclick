from fastapi import APIRouter

from app.routers.health import router as health_router
from app.routers.quotation_router import router as quotation_router
from app.routers.shipment_router import router as shipment_router
from app.routers.cancellation_router import router as cancellation_router
from app.routers.track_router import router as track_router

api_router = APIRouter()

# Registrar cada router individual
api_router.include_router(health_router)
api_router.include_router(quotation_router)
api_router.include_router(shipment_router)
api_router.include_router(cancellation_router)
api_router.include_router(track_router)