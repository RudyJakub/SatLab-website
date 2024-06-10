from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:123@db:3306/satlab")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
