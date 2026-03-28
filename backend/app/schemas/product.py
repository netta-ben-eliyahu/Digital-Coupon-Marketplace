import uuid
from pydantic import BaseModel, Field
from app.models.coupon import CouponValueType


class CouponCreate(BaseModel):

    name: str
    description: str
    image_url: str
    cost_price: float = Field(ge=0, description="Cost price must be non-negative")
    margin_percentage: float = Field(ge=0, description="Margin percentage must be non-negative")
    value_type: CouponValueType
    value: str

   

    
    
class CouponUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    image_url: str | None = None
    cost_price: float | None = Field(default=None, ge=0, description="Cost price must be non-negative")
    margin_percentage: float | None = Field(default=None, ge=0, description="Margin percentage must be non-negative")
    value: str | None = None


class ProductPublicResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    image_url: str
    price: float

    class Config:
        from_attributes = True


class CouponAdminResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    image_url: str
    cost_price: float
    margin_percentage: float
    minimum_sell_price: float
    is_sold: bool
    value_type: CouponValueType
    value: str

    class Config:
        from_attributes = True