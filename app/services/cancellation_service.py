import os
import requests
from typing import List
from fastapi import HTTPException, status

from app.schemas.schemas import (
    CancellationRequest,
    CancellationResponse
)


class CancellationService:
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
    
    def cancel_shipments(
        self,
        idOrders: List[int]
    ) -> CancellationResponse:
        """
        Cancel shipments by order IDs.
        """
        endpoint = f"{self.url}/cancellation/batch/order"

        payload = {"idOrders": idOrders}
        print("payload", payload)
        try:
            response = requests.post(
                endpoint, json=payload, headers=self.headers, timeout=30
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


        # try:
        #     return {
        #         "status": "OK",
        #         "status_codes": [200],
        #         "status_messages": [
        #             {
        #                 "request": "Request processed."
        #             }
        #         ],
        #         "data": {
        #             "not_valid_orders": [],
        #             "only_cancel_orders": [],
        #             "to_refund_orders": sorted(idOrders)
        #         }
        #     }

        # except Exception as e:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail=f"Error cancelling shipments: {str(e)}"
        #     )