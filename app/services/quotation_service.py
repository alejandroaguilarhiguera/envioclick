import requests
import os

from fastapi import HTTPException, status
from app.schemas.schemas import QuotationRequest
from app.schemas.schemas import Quotation, QuotationResponse

class QuotationService:
    def __init__(self):
        self.api_key = os.getenv("ENVIOCLICK_API_KEY")
        self.user_agent = os.getenv("ENVIOCLICK_USER_AGENT")
        self.url = os.getenv("ENVIOCLICK_URL")
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        self.endpoint = f"{self.url}/quotation"
    
    def get_quotation(self, quotation_in: QuotationRequest) -> QuotationResponse:
        """Retrieve all quotations."""
        payload = quotation_in.model_dump(by_alias=True)
        try:
            response = requests.post(
                self.endpoint, json=payload, headers=self.headers, timeout=30
            )
            if response.status_code >= 400:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error retrieving quotations: {response.text}",
                )
            return response.json()
        except requests.exceptions.RequestException as e:
          print("Error de conexión con Envíoclick:", e)
          raise HTTPException(
              status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
              detail="No se pudo establecer comunicación con el servicio de envíos.",
          )