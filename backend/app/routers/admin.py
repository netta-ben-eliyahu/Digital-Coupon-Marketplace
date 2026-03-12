from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_admin
from app.schemas.product import CouponCreate, CouponUpdate, CouponAdminResponse
from app.services import product_service

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"],
    dependencies=[Depends(get_admin)],
)

@router.get("/coupons", response_model=list[CouponAdminResponse])
def list_coupons(db: Session = Depends(get_db)):
    return product_service.get_all_products_admin(db)

@router.get("/coupons/{coupon_id}", response_model=CouponAdminResponse)
def get_coupon(coupon_id: str, db: Session = Depends(get_db)):
    return product_service.get_product_by_id(db, coupon_id)

@router.post("/coupons", response_model=CouponAdminResponse, status_code=status.HTTP_201_CREATED)
def create_coupon(coupon_data: CouponCreate, db: Session = Depends(get_db)):
    return product_service.create_coupon(db, coupon_data)

@router.patch("/coupons/{coupon_id}", response_model=CouponAdminResponse)
def update_coupon(coupon_id: str, coupon_data: CouponUpdate, db: Session = Depends(get_db)):
    return product_service.update_coupon(db, coupon_id, coupon_data)

@router.delete("/coupons/{coupon_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coupon(coupon_id: str, db: Session = Depends(get_db)):
    product_service.delete_coupon(db, coupon_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)