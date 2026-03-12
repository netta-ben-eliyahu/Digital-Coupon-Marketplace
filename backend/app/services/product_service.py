from sqlalchemy.orm import Session
from app.models.coupon import Coupon
from app.exceptions import ProductNotFoundException
from app.models.product import ProductType
from app.schemas.product import CouponCreate, CouponUpdate

def get_available_products(db: Session) -> list[Coupon]:
    return db.query(Coupon).filter(Coupon.is_sold == False).all()       

def get_product_by_id(db: Session, product_id: str) -> Coupon:
    product = db.query(Coupon).filter(Coupon.id == product_id).first()
    if not product:
        raise ProductNotFoundException()
    return product

def get_all_products_admin(db: Session) -> list[Coupon]:
    return db.query(Coupon).all()   

def create_coupon(db: Session, coupon_data: CouponCreate) -> Coupon:
    minimum_sell_price = coupon_data.cost_price * (1 + coupon_data.margin_percentage / 100)
    new_coupon = Coupon(
        **coupon_data.model_dump(),
        type=ProductType.COUPON,
        minimum_sell_price=minimum_sell_price
    )
    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)
    return new_coupon
    
    
def update_coupon(db: Session, coupon_id: str, coupon_data) -> Coupon:
    coupon = get_product_by_id(db, coupon_id)
    for key, value in coupon_data.model_dump(exclude_unset=True).items():
        setattr(coupon, key, value)
    if coupon_data.cost_price is not None or coupon_data.margin_percentage is not None:
        coupon.minimum_sell_price = coupon.cost_price * (1 + coupon.margin_percentage / 100)
    db.commit()
    db.refresh(coupon)
    return coupon

def delete_coupon(db: Session, coupon_id: str) -> None:
    coupon = get_product_by_id(db, coupon_id)
    db.delete(coupon)
    db.commit()
