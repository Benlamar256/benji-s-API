from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'mysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#while True:
   # try:
        #conn = mysql.connector.connect(host="127.0.0.1",user="root",password="Benja&256")    
        #cursor = conn.cursor()
        #print("database connection was successfull!")
        #break
    #except Exception as error:
        #print("database connection failed")
        #print("error",error)
        #time.sleep(2)