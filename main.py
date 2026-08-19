from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import models
import image_upload_endpoint
from database import engine
from routers import student, class_route, auth, post
from contextlib import asynccontextmanager
from init_db import init_admin
from middleware import LoggingMiddleware



@asynccontextmanager
async def lifespan( app: FastAPI):
    init_admin()
    yield
app = FastAPI(lifespan=lifespan)
models.Base.metadata.create_all(bind=engine) 

#middleware part
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers= ["*"]
)

app.include_router(student.router)
app.include_router(class_route.router)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(image_upload_endpoint.router)
app.mount("/static",StaticFiles(directory="static"),name="static")
@app.get("/")
def home():
    return {"message":"Welcome to School API"}


