from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from config import settings
import database, models, schemas
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error = False)

#this is for authorization box
bearer_scheme = HTTPBearer(auto_error  = False)


def get_current_user(oauth2_token: str= Depends(oauth2_scheme),bearer_creds: HTTPAuthorizationCredentials = Depends(bearer_scheme), db:Session=Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )

    #accept a token from either scheme or which one was actually provided 
    token = oauth2_token or (bearer_creds.credentials if bearer_creds else None)
    if not token:
        raise credentials_exception
    
    try:
        payload= jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "access":
            raise credentials_exception
        
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    user = db.query(models.DBUser).filter(models.DBUser.id==user_id).first()
    if user is None:
        raise credentials_exception
    return user

def require_admin(current_user:models.DBUser = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            details = "Admin access required ",
        )
    return current_user 