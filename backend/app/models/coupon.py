from sqlalchemy import Column, Numeric, Boolean, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.product import Product,ProductType


class CouponValueType(enum.Enum):
    STRING = "STRING"
    IMAGE = "IMAGE"


class Coupon(Product):
    __tablename__ = "coupons"
    id = Column(UUID(as_uuid=True),ForeignKey("products.id"), primary_key=True)
    cost_price = Column(Numeric(10, 2), nullable=False)
    margin_percentage = Column(Numeric(10, 2), nullable=False)
    minimum_sell_price = Column(Numeric(10, 2), nullable=False)
    is_sold = Column(Boolean, default=False)
    value_type = Column(Enum(CouponValueType), nullable=False)
    value = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": ProductType.COUPON
    }
