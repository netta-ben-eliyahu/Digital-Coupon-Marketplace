from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.dependencies import get_current_reseller
from app.services import product_service
from app.schemas.product import ProductPublicResponse
from app.schemas.purchase import PurchaseRequest, PurchaseResponse
from app.services import purchase_service

router = APIRouter(prefix="/api/v1", tags=["Reseller"]) 

@router.get("/products", response_model=list[ProductPublicResponse])
def list_products(db: Session = Depends(get_db), _ = Depends(get_current_reseller)):
    products = product_service.get_available_products(db)
    return [
        ProductPublicResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            image_url=p.image_url,
            price=float(p.minimum_sell_price)
        )
        for p in products
    ]

@router.get("/products/{product_id}", response_model=ProductPublicResponse)
def get_product(product_id: UUID, db: Session = Depends(get_db), _ = Depends(get_current_reseller)):
    product = product_service.get_product_by_id(db, product_id)
    return ProductPublicResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        image_url=product.image_url,
        price=float(product.minimum_sell_price)
    )      


# reseller.py
@router.post("/products/{product_id}/purchase", response_model=PurchaseResponse)
def purchase_product(
    product_id: UUID,
    purchase_request: PurchaseRequest,
    db: Session = Depends(get_db),
    _=Depends(get_current_reseller),
):
    return purchase_service.purchase_reseller(db, product_id, purchase_request.reseller_price)