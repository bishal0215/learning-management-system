from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
import models
import database
import schemas
router = APIRouter(
    prefix="/classes",
    tags=["Classes"]
)

@router.post("/")
def creare_class(cls: schemas.ClassSchema, db:Session = Depends(database.get_db)):
    db_class = db.query(models.DBClass).filter(models.DBClass.name == cls.name).first()
    if db_class:
        raise HTTPException(status_code=400, detail="this class is already exits")
    new_class = models.DBClass(name=cls.name, section=cls.section)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

@router.get("/")
def get_all_classes(db:Session = Depends(database.get_db)):
    return db.query(models.DBClass).all() 
