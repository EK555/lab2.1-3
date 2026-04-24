import jwt
from datetime import datetime, timedelta
import secrets
from app.core.config import settings

def generate_access_token(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_EXPIRES_MINUTES),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.JWT_ACCESS_SECRET, algorithm='HS256')

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)

def verify_access_token(token: str):
    try:
        return jwt.decode(token, settings.JWT_ACCESS_SECRET, algorithms=['HS256'])
    except:
        return None