from sqlalchemy.orm import Session
from app.models.coupon import Coupon
from app.schemas.purchase import PurchaseResponse
from app.exceptions import (
    ProductNotFoundException,
    ProductAlreadySoldException,
    ResellerPriceTooLowException
)


def purchase_reseller(db: Session, product_id: str, reseller_price: float) -> PurchaseResponse:

    coupon = db.query(Coupon).filter(Coupon.id == product_id).with_for_update().first()
    if not coupon:
        raise ProductNotFoundException()
    if coupon.is_sold:
        raise ProductAlreadySoldException()
    if reseller_price < float(coupon.minimum_sell_price):
        raise ResellerPriceTooLowException()
    coupon.is_sold = True
    db.commit()
    db.refresh(coupon)
    return PurchaseResponse(product_id=coupon.id, final_price =reseller_price, value_type=coupon.value_type, value=coupon.value)


def purchase_customer(db: Session, product_id: str) -> PurchaseResponse:
    coupon = db.query(Coupon).filter(Coupon.id == product_id).with_for_update().first()
    if not coupon:
        raise ProductNotFoundException()
    if coupon.is_sold:
        raise ProductAlreadySoldException()
    coupon.is_sold = True
    db.commit()
    db.refresh(coupon)
    return PurchaseResponse(product_id=coupon.id, final_price=float(coupon.minimum_sell_price), value_type=coupon.value_type, value=coupon.value)    