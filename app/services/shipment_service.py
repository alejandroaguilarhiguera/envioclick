import os
import requests
from fastapi import HTTPException, status

from app.schemas.schemas import ShipmentRequest

class ShipmentService:
    def __init__(self):
        self.api_key = os.getenv("ENVIOCLICK_API_KEY")
        self.user_agent = os.getenv("ENVIOCLICK_USER_AGENT")
        self.url = os.getenv("ENVIOCLICK_URL")
        self.sandbox_url = os.getenv("ENVIOCLICK_SANDBOX_URL")
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        if self.sandbox_url:
            self.url = self.sandbox_url
    def create_shipment(self, shipment_in: ShipmentRequest):
        """
        Create a shipment.
        """
        self.endpoint = f"{self.url}/shipment"

        payload = shipment_in.model_dump(mode="json", by_alias=True)
        try:
            response = requests.post(
                self.endpoint, json=payload, headers=self.headers, timeout=30
            )
            if response.status_code >= 400:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.text,
                )
            return response.json()
        except requests.exceptions.RequestException as e:
          print("Error de conexión con Envíoclick:", e)
          raise HTTPException(
              status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
              detail="No se pudo establecer comunicación con el servicio de envíos.",
          )
