from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    age = Column(Integer)
    stat = Column(Integer)
    


class Story(Base):
    __tablename__ = 'Stories'
    id = Column(Integer, primary_key=True)    
    name = Column(String)
    writer = Column(String)
    story = Column (String)
    pic = Column(Integer)
    likes = Column(Integer)
    date = Column(Integer)

