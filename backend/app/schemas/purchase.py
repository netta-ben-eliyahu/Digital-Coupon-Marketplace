import uuid
from pydantic import BaseModel
from app.models.coupon import CouponValueType

class PurchaseRequest(BaseModel):
    reseller_price: float 

    class Config:
        from_attributes = True  


class PurchaseResponse(BaseModel):
    product_id: uuid.UUID
    final_price: float
    value_type: CouponValueType
    value: str

    class Config:
        from_attributes = True
