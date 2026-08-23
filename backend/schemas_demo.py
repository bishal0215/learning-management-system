from pydantic import BaseModel, Field , field_validator
from typing import Optional

class CategorySchema(BaseModel):
    name:str=Field(..., min_length=2, max_length=30)
    description: Optional[str] = Field(None, max_length=200)

class PostCreate(BaseModel):
    title:str=Field(
        ...,
        min_length=3,
        max_length=100,
        description="The title of the post(3-100 characters)"
    )
    content:str = Field(..., min_length=10)
    rating: int= Field(default=5, ge=1, le=5)

    category:Optional[CategorySchema] = None

class UserRegister(BaseModel):
    username: str
    password:str
    @field_validator('username')
    @classmethod
    def username_must_be_alphanumeric(cls, value:str):
        if not value.isalnum():
            raise ValueError('Username must contain only letters and numbers')
        return value.lower()
    