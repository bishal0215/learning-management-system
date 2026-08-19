from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import schemas

router = APIRouter (
    prefix="/students",
    tags=["Students"]
)

@router.get("/", response_model=list[schemas.StudentResponseSchema])
def get_all_students(db: Session = Depends(database.get_db)):
    return db.query(models.DBStudent).all()

@router.post("/")
def create_student(student: schemas.StudentResponseSchema, db: Session = Depends(database.get_db)):
    db_student = db.query(models.DBStudent).filter(models.DBStudent.roll_no == student.roll_no).first()
    if db_student:
        raise HTTPException(status_code=400, detail="this roll no is already exit!")
    db_student_email = db.query(models.DBStudent).filter(models.DBStudent.email==student.email).first()

    if db_student_email:
        raise HTTPException(status_code=400, detail="this email is already exit!")
    
    db_class = db.query(models.DBClass).filter(models.DBClass.id==student.class_id).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="this class not found")
    
    new_student = models.DBStudent(name=student.name, roll_no=student.roll_no, email = student.email, is_active=student.is_active, age = student.age, class_id = student.class_id)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student 

@router.get("/{student_id}")
def get_student_by_id(student_id: int, db: Session = Depends(database.get_db)):
    student = db.query(models.DBStudent).filter(models.DBStudent.id==student_id).first()
    if not student:
       raise HTTPException(
           status_code=404,
           detail=f"ID {student_id} not found "
       )
    return student 

@router.patch("/{student_id}",response_model=schemas.StudentResponseSchema)
def update_student_partial(
    student_id:int,
    student_data: schemas.StudentUpdateSchema,
    db: Session = Depends(database.get_db)
):
    db_student = db.query(models.DBStudent).filter(models.DBStudent.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="not found")
    update_data = student_data.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_student,key,value)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/{student_id}")
def del_student_by_id(student_id: int, db: Session = Depends(database.get_db)):
    student = db.query(models.DBStudent).filter(models.DBStudent.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=404,
            detail= f"ID {student_id} not found"
        )
    db.delete(student)
    db.commit()
    return{"message":f"ID {student_id} removed successfully"}
        
