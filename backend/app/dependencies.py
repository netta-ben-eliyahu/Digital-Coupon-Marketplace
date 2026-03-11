from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.reseller import Reseller
from app.exceptions import UnauthorizedException
from app.config import settings


security = HTTPBearer()


def get_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != settings.ADMIN_TOKEN:
        raise UnauthorizedException()
    return True

def get_current_reseller(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    reseller = db.query(Reseller).filter(Reseller.token==token).first()
    if not reseller:
        raise UnauthorizedException()
    return reseller
