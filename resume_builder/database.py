from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQL_ALCHEMY_DATABSE_URL = "postgresql://shinus:alokin1234##@localhost/resume_builder"

engine = create_engine(SQL_ALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
