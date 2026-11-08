
import os
from typing import List
import requests
from fastapi import HTTPException, status
from app.schemas.schemas import TrackingCodeRequest


class TrackService:
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

    def get_by_id(self, track_id: str):
        """
        get tracking by id
        """
        endpoint = f"{self.url}/track-by-orders/{track_id}"
        try:
            response = requests.get(
                endpoint, headers=self.headers, timeout=30
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
        #         "status_codes": [
        #             200
        #         ],
        #         "status_messages": [
        #             {
        #                 "request": "Request processed."
        #             }
        #         ],
        #         "data": {
        #             "status": "Pendiente de Recolección",
        #             "statusDetail": "Pendiente de Recolección",
        #             "arrivalDate": None,
        #             "realPickupDate": None,
        #             "realDeliveryDate": None,
        #             "receivedBy": None
        #         }
        #     }

        # except Exception as e:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail=f"Error get tracking:{track_id} {str(e)}"
        #     )
    def get_by_request(self, trackingCode: str):
        """
        get tracking by request
        """
        endpoint = f"{self.url}/track"
        payload = {"trackingCode": trackingCode}

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
        #         "status_codes": [
        #             200
        #         ],
        #         "status_messages": [
        #             {
        #                 "request": "Request processed."
        #             }
        #         ],
        #         "data": {
        #             "status": "Pendiente de Recolección",
        #             "statusDetail": "Pendiente de Recolección",
        #             "arrivalDate": None,
        #             "realPickupDate": None,
        #             "realDeliveryDate": None,
        #             "receivedBy": None
        #         }
        #     }

        # except Exception as e:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail=f"Error get tracking: {str(e)}"
        #     )
    def get_tracking_codes(self, trackingCodes: List[str]):
        """
        get tracking by request
        """
        endpoint = f"{self.url}/track-batch"

        payload = {"trackingCodes": trackingCodes}
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
        #     return   {
        #         "status": "OK",
        #         "status_codes": [
        #             200
        #         ],
        #         "status_messages": [
        #             {
        #                 "request": "Request processed."
        #             }
        #         ],
        #         "data": {
        #             "8058630274616780407276": {
        #                 "status": "Pendiente de Recolección",
        #                 "statusDetail": "Pendiente de Recolección",
        #                 "arrivalDate": None,
        #                 "realPickupDate": None,
        #                 "realDeliveryDate": None,
        #                 "receivedBy": None
        #             },
        #             "0058630274616780407275": {
        #                 "status": "Pendiente de Recolección",
        #                 "statusDetail": "Pendiente de Recolección",
        #                 "arrivalDate": None,
        #                 "realPickupDate": None,
        #                 "realDeliveryDate": None,
        #                 "receivedBy": None
        #             }
        #         }
        #     }

        # except Exception as e:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail=f"Error get tracking: {str(e)}"
        #     )
    def get_by_orders(self, orders: List[int]):
        """
        get tracking by orders
        """
        endpoint = f"{self.url}/track-by-orders"
        payload = {"orders": orders}
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
        #     return   {
        #         "status": "OK",
        #         "status_codes": [
        #             200
        #         ],
        #         "status_messages": [
        #             {
        #                 "request": "Request processed."
        #             }
        #         ],
        #         "data": {
        #             "89758": {
        #                 "status": "Entregado",
        #                 "statusDetail": "ENTREGADA",
        #                 "arrivalDate": "2019-07-29 00:00:00",
        #                 "realPickupDate": "2019-07-26 16:08:42",
        #                 "realDeliveryDate": "2019-07-29 00:00:00",
        #                 "receivedBy": "No Tiene Registro"
        #             }
        #         }
        #     }

        # except Exception as e:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail=f"Error get tracking: {str(e)}"
        #     )