from fastapi import FastAPI,Depends,HTTPException,status,Request,Response
import models,schema,views,calculation
from db_config import SessionLocal,engine
from sqlalchemy.orm import Session
from typing import Dict
from starlette.middleware.sessions import SessionMiddleware



models.Base.metadata.create_all(bind=engine)



app = FastAPI()

# app.add_middleware(SessionManager, secret_key="your_secret_key")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/hello_world')
def hello_world():
    return {"message":"Hello world"}

@app.post('/add_teacher',response_model = schema.Teacher)
def add_teacher(teacher:schema.TeacherCreate,db: Session = Depends(get_db)):
    try:
        get_user = views.get_teacher_by_username(db, Username=teacher.Username)
        if get_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        return views.add_teacher(db=db, teacher=teacher)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding the teacher.",
        ) from e

@app.get('/get_teachers',response_model = list[schema.Teacher])
def get_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        teachers = views.get_teachers(db, skip=skip, limit=limit)
        return teachers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving teachers.",
        ) from e


@app.put('/update_teacher/{id}',response_model = schema.Teacher)
def update_teachers(id:int,teacher_update: schema.TeacherBase,db:Session=Depends(get_db)):
    print('teacher',teacher_update)
    teacher = views.update_teacher(db=db,id=id,teacher_update=teacher_update)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@app.delete('/delete_teacher/{id}',response_model=Dict[str, str])
def delete_teachers(id:int,db:Session=Depends(get_db)):
    teacher = views.delete_teacher(id=id, db=db)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"Message":"Deleted Successfully"}

@app.post('/login', response_model=dict)
def login(login: schema.TeacherCreate, response: Response, db: Session = Depends(get_db)):
    return views.login_teacher(login=login, db=db, response=response)

@app.post('/logout')
def logout(response: Response):
    return views.logout(response=response)

@app.post('/add_student',response_model = schema.Student)
def add_student(student: schema.StudentCreate,db: Session = Depends(get_db)):
    return views.add_student(db=db,student=student)

@app.post('/assign_teacher/{id}', response_model=schema.Student)
def assign_teachers(id: int, student: schema.StudentUpdate, db: Session = Depends(get_db)):
    return views.assign_teacher(db=db, student=student, id=id)


@app.post('/distance/')
def get_distance(coordinates: schema.CoordinateInput):
    distance = calculation.calculate_distance(coordinates.lat1, coordinates.lon1, coordinates.lat2, coordinates.lon2)
    return {"distance": distance}
    
    
    
    

