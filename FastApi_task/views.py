from sqlalchemy.orm import Session
import models,schema
from fastapi import HTTPException, status
import bcrypt
from fastapi import Request,Depends
from fastapi import Response






def get_teacher_by_username(db: Session, Username: str):
    return db.query(models.Teacher).filter(models.Teacher.Username == Username).first()

def add_teacher(db:Session, teacher:schema.TeacherCreate):
    print('in')
    Password =  teacher.Password
    teachers = models.Teacher(Name = teacher.Name,Subject = teacher.Subject,Username = teacher.Username,Password=Password)
    try:
        db.add(teachers)
        db.commit()
        db.refresh(teachers)
        return teachers
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding the teacher."
        ) from e
        

def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    try:
        teachers = db.query(models.Teacher).offset(skip).limit(limit).all()
        return teachers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving teachers.",
        ) from e

def update_teacher(db: Session,id:int,teacher_update: schema.TeacherBase):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if teacher:
        for attr, value in teacher_update.dict(exclude_unset=True).items():
            setattr(teacher, attr, value)
        db.commit()
        db.refresh(teacher)
        return teacher

def delete_teacher(db:Session,id:int):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if teacher:
        db.delete(teacher)
        db.commit()
    return {"Message":"Deleted Successfully"}


def login_teacher(login: schema.TeacherCreate, db: Session, response: Response):
    print('in view')
    teacher = db.query(models.Teacher).filter(models.Teacher.Username == login.Username, models.Teacher.Password == login.Password).first()
    print('tech', teacher)
    if teacher:
        # Successful login
        #session = request.session
        #session['username'] = login.Username
        
        response.set_cookie(key="username", value=login.Username,max_age = 36000) # Set timeout to 1 hour (in seconds)
        return {"message": "Login successful"}

    # Invalid credentials
    raise HTTPException(status_code=401, detail="Invalid username or password")


def logout(response: Response):
    # Clear the session cookie
    response.delete_cookie(key="username")
    return {"message": "Logout successful"}


def add_student(db:Session,student:schema.StudentCreate):
    if not student.Name or not student.Age:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please enter name and age."
        )
    try:
        students = models.Student(Name=student.Name,Age=student.Age)    
        db.add(students)
        db.commit()
        db.refresh(students)
        return students
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding the teacher."
        ) from e
        

def assign_teacher(db: Session, student:schema.StudentUpdate, id: int):
    student_model = db.query(models.Student).filter(models.Student.id == id).first()
    if not student_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    teach = db.query(models.Teacher).filter(models.Teacher.id == student.teacher_id).first()
    if not  teach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher with this id not found",
        )
        
    student_model.teacher_id = student.teacher_id
    db.commit()
    db.refresh(student_model)
    return student_model





    




    
    
    


    
    


    
    
