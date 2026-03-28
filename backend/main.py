from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions import AppException
from app.routers import admin, reseller, customer
from app.database import SessionLocal
from app.models.reseller import Reseller
from app.config import settings

app = FastAPI(title="Digital Coupon Marketplace")


@app.on_event("startup")
def seed_reseller():
    db = SessionLocal()
    try:
        exists = db.query(Reseller).filter(Reseller.token == settings.RESELLER_TOKEN).first()
        if not exists:
            db.add(Reseller(name="Default Reseller", token=settings.RESELLER_TOKEN))
            db.commit()
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_code": exc.error_code, "message": exc.message}
    )


app.include_router(reseller.router)
app.include_router(admin.router)
app.include_router(customer.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
