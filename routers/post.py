from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database import Base
from typing import List
import database, models, schemas 
from routers import oauth2
from exceptions import PostNotFoundException

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    current_user:models.DBUser=Depends(oauth2.get_current_user)
):
    new_post= models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/",response_model=List[schemas.PostResponse])
def get_posts(db:Session= Depends(database.get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id:int, db:Session=Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id ==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return post

@router.patch("/{id}", response_model=schemas.PostResponse)
def update_post(
    id : int,
    updated_post:schemas.PostUpdateSchema,
    db: Session = Depends(database.get_db),
    current_user: models.DBUser=Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform request action")
    update_data = updated_post.model_dump(exclude_unset = True)
    
    post_query.update(update_data, synchronize_session= False)
    db.commit()
    return post_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id:int,
    db:Session = Depends(database.get_db),
    current_user: models.DBUser = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id ==id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")

    if post.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
