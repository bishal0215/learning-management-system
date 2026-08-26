from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")
from config import settings


def hash_password(password: str) -> str:
    safe_password = password.encode('utf-8')[:72].decode('utf-8',errors='ignore')

    return pwd_context.hash(safe_password)

def verify_password(plain_password: str, hashed_password :str) -> bool:
    safe_password = plain_password.encode('utf-8')[:72].decode('utf-8',errors='ignore')

    return pwd_context.verify(safe_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) +timedelta(minutes= settings.access_token_expire_minutes)
    to_encode.update({"exp":expire, "type":"access"})
    encode_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encode_jwt

def create_refresh_token(data: dict): #its for refresh token
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) +timedelta(days= settings.refresh_token_expire_days)
    to_encode.update({"exp":expire, "type":"refresh"})
    encode_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encode_jwt
