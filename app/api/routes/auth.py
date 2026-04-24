from fastapi import APIRouter, Request, Response, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest, WhoamiResponse, UserResponse, MessageResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201, response_model=MessageResponse)
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = AuthService.register(db, data.email, data.password)
        return MessageResponse(message="Пользователь успешно зарегистрирован")
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.post("/login")
async def login(response: Response, data: LoginRequest, db: Session = Depends(get_db)):
    try:
        access_token, refresh_token, user = AuthService.login(db, data.email, data.password)
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=15 * 60
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=7 * 24 * 60 * 60
        )
        
        return {"message": "Вход выполнен успешно", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/refresh")
async def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get('refresh_token')
    
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Не предоставлен refresh token")
    
    try:
        new_access_token, new_refresh_token = AuthService.refresh(db, refresh_token)
        
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=15 * 60
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=7 * 24 * 60 * 60
        )
        
        return {"message": "Токены обновлены"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
async def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get('refresh_token')
    AuthService.logout(db, refresh_token)
    
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    return {"message": "Выход выполнен"}

@router.post("/logout-all")
async def logout_all(request: Request, response: Response, db: Session = Depends(get_db)):
    access_token = request.cookies.get('access_token')
    if access_token:
        user = AuthService.get_user_from_access_token(db, access_token)
        if user:
            AuthService.logout_all(db, user['id'])
    
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    return {"message": "Выход со всех устройств выполнен"}

@router.get("/whoami", response_model=WhoamiResponse)
async def whoami(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get('access_token')
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    user = AuthService.get_user_from_access_token(db, access_token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    return WhoamiResponse(user=UserResponse(**user))