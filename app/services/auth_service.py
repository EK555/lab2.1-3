from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.config import settings
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.utils.hash_utils import hash_password, verify_password
from app.utils.jwt_utils import generate_access_token, generate_refresh_token, verify_access_token
from app.utils.refresh_token_utils import hash_refresh_token

class AuthService:
    
    @staticmethod
    def register(db: Session, email: str, password: str):
        existing = db.query(User).filter(User.email == email, User.deleted_at.is_(None)).first()
        if existing:
            raise ValueError("Пользователь с таким email уже существует")
        
        password_hash = hash_password(password)
        user = User(email=email, password_hash=password_hash)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {"id": user.id, "email": user.email}
    
    @staticmethod
    def login(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email, User.deleted_at.is_(None)).first()
        
        if not user or not user.password_hash:
            raise ValueError("Неверный email или пароль")
        
        if not verify_password(password, user.password_hash):
            raise ValueError("Неверный email или пароль")
        
        access_token = generate_access_token(user.id)
        refresh_token = generate_refresh_token()
        refresh_token_hash = hash_refresh_token(refresh_token)
        expires_at = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_EXPIRES_DAYS)
        
        new_token = RefreshToken(
            user_id=user.id,
            token_hash=refresh_token_hash,
            expires_at=expires_at
        )
        db.add(new_token)
        db.commit()
        
        return access_token, refresh_token, {"id": user.id, "email": user.email}
    
    @staticmethod
    def refresh(db: Session, old_refresh_token: str):
        token_hash = hash_refresh_token(old_refresh_token)
        stored_token = db.query(RefreshToken).filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        ).first()
        
        if not stored_token:
            raise ValueError("Неверный или истекший refresh token")
        
        stored_token.revoked = True
        db.commit()
        
        new_access_token = generate_access_token(stored_token.user_id)
        new_refresh_token = generate_refresh_token()
        new_token_hash = hash_refresh_token(new_refresh_token)
        expires_at = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_EXPIRES_DAYS)
        
        new_token = RefreshToken(
            user_id=stored_token.user_id,
            token_hash=new_token_hash,
            expires_at=expires_at
        )
        db.add(new_token)
        db.commit()
        
        return new_access_token, new_refresh_token
    
    @staticmethod
    def logout(db: Session, refresh_token: str):
        if refresh_token:
            token_hash = hash_refresh_token(refresh_token)
            token = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
            if token:
                token.revoked = True
                db.commit()
    
    @staticmethod
    def logout_all(db: Session, user_id: int):
        db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False
        ).update({"revoked": True})
        db.commit()
    
    @staticmethod
    def get_user_from_access_token(db: Session, access_token: str):
        payload = verify_access_token(access_token)
        if not payload:
            return None
        
        user = db.query(User).filter(
            User.id == payload['user_id'],
            User.deleted_at.is_(None)
        ).first()
        
        if not user:
            return None
        
        return {"id": user.id, "email": user.email}