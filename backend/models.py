from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, DateTime, Table
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

class DBClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index= True)
    name = Column(String, unique= True, index= True)
    section = Column(String)
    students = relationship("DBStudent", back_populates="current_class")

class DBStudent(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, index=True)
    age = Column(Integer, index=True)
    roll_no = Column(Integer, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    class_id = Column(Integer, ForeignKey("classes.id"))
    current_class = relationship("DBClass", back_populates="students")

class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable = False)
    email =  Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean,default=True)
    is_superuser = Column(Boolean, default=False)
    bio = Column(String, nullable=True)

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id",Integer, ForeignKey("posts.id"), primary_key = True),
    Column("tag_id",Integer, ForeignKey("tags.id"), primary_key = True),

)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key =True, index=True)
    name = Column(String, unique = True, index = True, nullable = False)
    posts = relationship("Post", secondary = post_tags, back_populates ="tags")
    

#its for posts
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index= True)
    title = Column(String, nullable=False)
    content = Column(String, nullable= False)
    published = Column(Boolean, server_default='True',nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    owner = relationship(DBUser)
    image_url = Column(String, nullable= True)
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    created_at = Column(TIMESTAMP, server_default=expression.text("CURRENT_TIMESTAMP"),nullable=False)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index= True)
    token = Column(String, unique= True, index= True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id",ondelete = "CASCADE"), nullable=False)
    expires_at = Column(TIMESTAMP, nullable= False)
    revoked = Column(Boolean, default= False)