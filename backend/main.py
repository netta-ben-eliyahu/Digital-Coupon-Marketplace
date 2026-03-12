from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions import AppException
from app.routers import admin, reseller, customer

app = FastAPI(title="Digital Coupon Marketplace")

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
