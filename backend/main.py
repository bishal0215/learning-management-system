from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import models
import image_upload_endpoint
from database import engine
from routers import student, class_route, auth, post , google_auth
from contextlib import asynccontextmanager
from init_db import init_admin
from middleware import LoggingMiddleware
from config import settings



@asynccontextmanager
async def lifespan( app: FastAPI):
    init_admin()
    yield

app = FastAPI(lifespan=lifespan)
models.Base.metadata.create_all(bind=engine) 
#requrired by authlib to store temporary ouath state during the redirect to/from google, uses existing secret key
app.add_middleware(SessionMiddleware, secret_key = settings.secret_key)

#middleware part
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers= ["*"]
)
#custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code = 404,
        content={"message":f"the recource at '{request.url.path}' was not found"},

    )

app.include_router(student.router)
app.include_router(class_route.router)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(google_auth.router)
app.include_router(image_upload_endpoint.router)
app.mount("/static",StaticFiles(directory="static"),name="static")
@app.get("/")
def home():
    return {"message":"Welcome to School API"}


