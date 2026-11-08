from datetime import date
from typing import Optional, Union
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any


class QuotationStatusMessage(BaseModel):
    request: str


class QuotationInsurance(BaseModel):
    contentValue: float
    amountInsurance: float
    insurance: float


class QuotationRate(BaseModel):
    idRate: int
    idProduct: int
    product: str
    idCarrier: int
    carrier: str
    total: float
    deliveryDays: int
    deliveryType: str
    quotationType: str
    distance: Optional[float] = None
    cod: bool


class QuotationPackage(BaseModel):
    weight: float
    length: float
    height: float
    width: float

class Quotation(BaseModel):
    insurance: QuotationInsurance
    rates: List[QuotationRate]
    idCarriersNoWsResult: List[int]
    package: QuotationPackage
    originZipCode: str
    destinationZipCode: str



class QuotationResponse(BaseModel):
    status: str
    status_codes: List[int]
    status_messages: List[QuotationStatusMessage]
    data: Quotation

class PackageRequest(BaseModel):
    description: str
    contentValue: float = Field(gt=0)
    weight: float = Field(gt=0)
    length: float = Field(gt=0)
    height: float = Field(gt=0)
    width: float = Field(gt=0)


class QuotationRequest(BaseModel):
    origin_address: str
    origin_number: str
    origin_zip_code: str
    origin_suburb: str

    destination_address: str
    destination_number: str
    destination_zip_code: str
    destination_suburb: str

    package: PackageRequest


# =====================
# Shipment Models
# =====================


# Shipment Package Items
class ShipmentPackageItem(BaseModel):
    c_ClaveUnidadPeso: str
    c_ClaveProdServCP: str
    c_MaterialPeligroso: Optional[str] = None
    c_TipoEmbalaje: Optional[str] = None
    contentValue: float = Field(gt=0)
    units: int = Field(gt=0)


# Shipment Package
class ShipmentPackage(BaseModel):
    description: str
    contentValue: float = Field(gt=0)
    weight: float = Field(gt=0)
    length: float = Field(gt=0)
    height: float = Field(gt=0)
    width: float = Field(gt=0)
    items: List[ShipmentPackageItem]


# Shipment Address
class ShipmentAddress(BaseModel):
    company: Optional[str] = None
    rfc: str
    firstName: str
    lastName: str
    email: str
    phone: str
    street: str
    number: str
    intNumber: Optional[str] = None
    suburb: str
    crossStreet: Optional[str] = None
    zipCode: str
    reference: Optional[str] = None
    observations: Optional[str] = None


# Shipment Request
class ShipmentRequest(BaseModel):
    idRate: int
    myShipmentReference: Optional[str] = None
    requestPickup: bool
    pickupDate: Optional[date] = None
    insurance: bool
    package: ShipmentPackage
    origin: ShipmentAddress
    destination: ShipmentAddress

class ShipmentStatusMessage(BaseModel):
    request: str

class ShipmentPackageItemResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    c_ClaveUnidadPeso: str = Field(..., alias="weight_unit_key")
    c_ClaveProdServCP: str = Field(..., alias="product_key")
    c_MaterialPeligroso: Optional[Any] = Field(None, alias="is_dangerous")
    c_TipoEmbalaje: Optional[str] = None
    contentValue: float = Field(..., alias="content_value", gt=0)
    units: int = Field(..., alias="number_of_units", gt=0)
    
class ShipmentPackageResponse(BaseModel):
    description: Optional[str] = None
    contentValue: Optional[float] = None
    weight: float
    length: float
    height: float
    width: float
    items: List[ShipmentPackageItemResponse]

class ShipmentDataResponse(BaseModel):
    idRate: int
    myShipmentReference: Optional[str] = None
    requestPickup: bool
    pickupDate: Optional[date] = None
    insurance: bool
    countryCode: Optional[str] = None
    
    # package: ShipmentPackage
    package: ShipmentPackageResponse
    origin: ShipmentAddress
    destination: ShipmentAddress

    guide: Optional[str] = None
    url: Optional[str] = None
    tracker: Optional[str] = None

    idOrder: int
    deliveryType: str
    deliveryDays: int

class ShipmentResponse(BaseModel):
    status: str
    status_codes: List[int]
    status_messages: List[ShipmentStatusMessage]
    data: ShipmentDataResponse


class CancellationRequest(BaseModel):
    idOrders: List[int] = Field(min_length=1)


class CancellationDataResponse(BaseModel):
    not_valid_orders: List[int]
    only_cancel_orders: List[int]
    to_refund_orders: List[int]


class CancellationResponse(BaseModel):
    status: str
    status_codes: List[int]
    status_messages: List[ShipmentStatusMessage]
    data: CancellationDataResponse

class TrackData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    status: str
    status_detail: str = Field(..., alias="statusDetail")
    arrival_date: Optional[str] = Field(None, alias="arrivalDate")
    real_pickup_date: Optional[str] = Field(None, alias="realPickupDate")
    real_delivery_date: Optional[str] = Field(None, alias="realDeliveryDate")
    received_by: Optional[Any] = Field(None, alias="receivedBy")  # Puede ser string o null

class TrackResponse(BaseModel):
    status: str
    status_codes: List[int]
    status_messages: List[Dict[str, str]]
    data: TrackData

class TrackingCodeRequest(BaseModel):
    trackingCode: str

class TrackingCodesRequest(BaseModel):
    trackingCodes: List[str]

class TrackDetail(BaseModel):
    status: Optional[str] = None
    statusDetail: Optional[str] = None
    arrivalDate: Optional[str] = None
    realPickupDate: Optional[str] = None
    realDeliveryDate: Optional[str] = None
    receivedBy: Optional[str] = None

class StatusMessage(BaseModel):
    request: str

class TrackBatchResponse(BaseModel):
    status: str
    status_codes: List[int]
    status_messages: List[StatusMessage]
    data: Union[Dict[str, TrackDetail], str, Any]

class TrackOrdersRequest(BaseModel):
    orders: List[int] = Field(..., min_length=1)
