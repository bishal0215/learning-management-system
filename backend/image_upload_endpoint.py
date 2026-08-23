from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
import shutil
import os
import database, models
from sqlalchemy.orm import Session

router = APIRouter()
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok= True)

@router.post("/posts/{id}/upload-image")
async def upload_post_image(id:int, file:UploadFile = File(...), db:Session = Depends(database.get_db)) :
    post = db.query(models.post).filter(models.Post.id ==id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail= f"Post with id {id} not found "
        )
    allowed_types = ["image/jpeg","image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code= 400,
            detail= " Invalid file type. only jpeg and png are allowed."

        )

    file_location = os.path.join(UPLOAD_DIR, f"post_{id}_{file.filename}")
    with open (file_location, "wb") as buffer :
        shutil.copyfileobj(file.file,buffer)

    image_url = f"/static/uploads/post_{id}_{file.filename}"
    post.image_url = image_url
    db.commit
    db.refresh(post)

    return{
        "filename":file.filename,
        "file_path":file_location,
        "url": image_url, 
        "content_type": file.content_type
    }