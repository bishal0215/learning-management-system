from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from authlib.integrations.starlette_client import OAuth
import secrets

import database, models, utils
from config import settings

router = APIRouter(
    prefix = "/auth/google",
    tags = ["Google Auth"]

)

ouath = OAuth()
ouath.register(
    name='google',
    client_id = settings.google_client_id,
    client_secret = settings.google_client_secret,
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs = {'scope':'openid email profile'},
)

@router.get("/login")
async def google_login(request:Request):
    redirect_url = request.url_for('google_callback')
    return await ouath.google.authorize_redirect(request, redirect_url)

@router.get("/callback")
async def google_callback(request:Request,db:Session = Depends(database.get_db)):
    try:
        token = await ouath.google.authorize_access_token(request)
    except Exception:
        raise HTTPException(status_code=401,detail="Google authentication failed")
    user_info =  token.get("userinfo")
    if not user_info or not user_info.get("email"):
        raise HTTPException(status_code = 400, details ="Could not get user info from Google")
    email = user_info["email"]

    #find the existing user by email or create a new one 

    user = db.query(models.DBUser).filter(models.DBUser.email == email).first()

    if not user:
        random_password = utils.hash_password(secrets.token_urlsafe(32))
        username_base = email.split("@")[0]
        #ensure username is unique
        username = username_base
        suffix = 1
        while db.query(models.DBUser).filter(models.DBUser.username == username).first():
            username = f"{username_base}{suffix}"
            suffix += 1
        user = models.DBUser(
            username = username,
            email = email,
            password = random_password,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    #issue our own token , same system as normal login
    access_token = utils.create_access_token(data={"user_id":user.id})
    refresh_token = utils.create_refresh_token(data={"user_id":user.id})
    db_token = models.RefreshToken(
        token = refresh_token,
        user_id = user.id,
        expires_at =  datetime.now(timezone.utc)+ timedelta(days=settings.refresh_token_expire_days),

    )
    db.add(db_token)
    db.commit()

    return{
        "access_token":access_token,
        "refresh_token": refresh_token,
        "token_type":"bearer",
    }