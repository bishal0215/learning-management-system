from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from datetime import datetime
class ClassSchema(BaseModel):
    id: int| None= None
    name:str
    section:str

    class Config:
        from_attributes = True

class StudentCreateSchema(BaseModel):
    name:str
    roll_no:int
    email:EmailStr
    age:int
    is_active:bool
    class_id:int
        
class StudentResponseSchema(BaseModel):
    id: int| None= None
    name:str
    roll_no:int
    email: EmailStr
    age: int
    is_active: bool = True
    class_id: int
    current_class: ClassSchema | None = None
    class Config:
        from_attributes = True

class UserCreateSchema(BaseModel):
    username : str
    email : EmailStr
    password :str

class UserResponseSchema(BaseModel):
    id:int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser:bool
    model_config = ConfigDict(from_attributes= True)

class StudentUpdateSchema(BaseModel):
    name: Optional[str] = None
    roll_no: Optional[int] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    is_active: Optional[bool] = None
    class_id: Optional[int] = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type:str

class TokenDataSchema(BaseModel):
    id: str | None=None

class RefreshRequestSchema(BaseModel):
    refresh_token: str
    
class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:str
    username:str

    class Config:
        from_attributes=True

class PostResponse(PostBase):
    id:int
    owner_id:int
    owner:UserOut
    image_url:Optional[str]=None
    created_at: datetime
    class Config : from_attributes = True

class PostUpdateSchema(BaseModel):
    title: Optional[str] =None
    content: Optional[str] = None
    published: Optional[bool]= None


