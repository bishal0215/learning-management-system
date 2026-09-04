import pytest 
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args = {"check_same_thread":False}

)
TestingSessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
def override_get_db():
    db= TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestClient(app)

@pytest.fixture
def existing_user(client):
    client.post(
        "/auth/signup",
        json={
            "username": "loginuser",
            "email": "loginuser@example.com",
            "password": "correctpassword123",
        },
    )
    return {"username": "loginuser", "password": "correctpassword123"}