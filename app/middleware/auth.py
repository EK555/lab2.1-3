from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import AuthService

async def authenticate(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get('access_token')
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Не предоставлен access token")
    
    user = AuthService.get_user_from_access_token(db, access_token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Неверный или истекший токен")
    
    request.state.user = user
    return True