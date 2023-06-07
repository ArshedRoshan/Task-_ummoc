from sqlalchemy import Integer,String,ForeignKey,Column
from db_config import Base

class Teacher(Base):
    __tablename__ = "teacher"
    
    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String,index = True)
    Subject = Column(String,index = True)
    Username = Column(String,index = True)
    Password = Column(String)
    
    

class Student(Base):
    __tablename__ = "student"
    
    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String,index = True)
    Age  = Column(Integer,index = True)
    teacher_id = Column(Integer,ForeignKey("teacher.id"),nullable=True)
    
    
    
    
    