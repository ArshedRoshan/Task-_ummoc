from pydantic import BaseModel,validator
from typing import Optional


class TeacherBase(BaseModel):
    Name:str
    Subject:str
    Username:str
    
class TeacherCreate(TeacherBase):
    Password : str
    Name: Optional[str] = None
    Subject: Optional[str] = None

class Teacher(TeacherBase):
    id:int
    
    class Config:
        orm_mode = True


class StudentBase(BaseModel):
    Name: str
    Age: int
    

class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    teacher_id: Optional[int]
    Name : Optional[str] = None
    Age  : Optional[str] = None

class Student(StudentBase):
    id : int
    teacher_id: Optional[int]
    
    class Config:
        orm_mode = True
        
   
        
        
class CoordinateInput(BaseModel):
    lat1: float
    lon1: float
    lat2: float
    lon2: float