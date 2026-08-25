from fastapi import APIRouter , Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import models, schemas, database, utils 
from sqlalchemy import or_
from config import settings
from . import oauth2


router = APIRouter(
    prefix = "/auth",
    tags = ["Authentications"]
)

@router.get("/me", response_model=schemas.UserResponseSchema)
def get_my_profile(current_user: models.DBUser = Depends(oauth2.get_current_user)):
    return current_user
#get all users 
@router.get("/users",response_model= List[schemas.UserResponseSchema])
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.DBUser).all()
    return users

#get all users by id 
@router.get("/{user_id}")
def get_user_by_id(user_id : int ,db:Session= Depends(database.get_db)):
    user = db.query(models.DBUser).filter(models.DBUser.id==user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} not found"
        )
    return user

#admin user 
@router.post("/signup",response_model = schemas.UserResponseSchema, status_code = status.HTTP_201_CREATED)
def signup(user_data: schemas.UserCreateSchema, db: Session= Depends(database.get_db)):
    existing_user = db.query(models.DBUser).filter(
            or_(
                models.DBUser.username == user_data.username,
                models.DBUser.email == user_data.email
                )
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="this  username or email is already used")
    hashed_pwd = utils.hash_password(user_data.password)
    new_user = models.DBUser(
        username = user_data.username,
        email = user_data.email,
        password = hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login",response_model=schemas.TokenSchema)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db:Session = Depends(database.get_db)
):
    user = db.query(models.DBUser).filter(
        models.DBUser.username == user_credentials.username
    ).first()

    if not user:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    access_token = utils.create_access_token(data={"user_id":user.id})
    refresh_token = utils.create_access_token(data= {"user_id":user.id})

    #store refresh token so it can be checked/ revoked later
    db_token = models.RefreshToken(
        token = refresh_token,
        user_id = user.id,
        expires_at = datetime.now(timezone.utc)+timedelta(days= settings.refresh_token_expire_days),

    )
    db.add(db_token)
    db.commit()
    return{"access_token":access_token, "refresh_token":refresh_token, "token_type":"bearer"}

@router.post("/refresh",response_model=schemas.TokenSchema)
def refresh_token(
    request: schemas.RefreshRequestSchema,
    db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid or expire refresh token",
    )
    try:
        payload = jwt.decode(request.refresh_token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise credentials_exception
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # check its still valid in the DB

    db_token =  db.query(models.RefreshToken).filter(
        models.RefreshToken.token == request.refresh_token,
        models.RefreshToken.revoked== False,
    ).first()

    if not db_token:
        raise HTTPException(status_code=401, detail="Refresh token revoked or not found")

    #now new access token
    new_access_token = utils.create_access_token(data={"user_id":user_id})
    new_refresh_token = utils.create_refresh_token(data={"user_id":user_id})
    db_token.revoked = True
    new_db_token = models.RefreshToken(
        token= new_refresh_token,
        user_id = user_id,
        expires_at = datetime.now(timezone.utc) + timedelta(days= settings.refresh_token_expire_days),

    )
    db.add(new_db_token)
    db.commit()

    return{
        "access_token":new_access_token,
        "refresh_token":new_refresh_token,
        "token_type":"bearer",
    }

@router.post("/logout")
def logout(
    request:schemas.RefreshRequestSchema,
    db:Session= Depends(database.get_db)
):
    db_token = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == request.refresh_token
    ).first()
    if db_token:
        db_token.revoked= True
        db.commit()

    return{"message":"logged out successfully"}

