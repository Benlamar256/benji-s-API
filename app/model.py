from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "Patient_Details"

    Patient_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    Full_name = Column(String(100), nullable=False)
    test_date = Column(String(255), nullable=False)
    Age = Column(Integer, nullable=False)
    sex = Column(String(100), nullable=False)
    Test_results=Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    ower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), autoincrement=True, nullable=False)
    onwer = relationship("User")

class User(Base):
    __tablename__= "users"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    Full_Name = Column(String(100), unique=True, nullable= False)
    email = Column(String(100), unique=True, nullable= False)
    password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))




                
                
                            

