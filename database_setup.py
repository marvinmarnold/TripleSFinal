from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine
import os

DATABASE_URL = os.environ['DATABASE_URL']

Base = declarative_base()
engine = create_engine(DATABASE_URL, convert_unicode=True)

Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = DBSession.query_property()

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

Base.metadata.create_all(engine)

#class Comment(Base):
    #__tablename__ = 'Comments'
    #id = Column(Integer, primary_key=True)
 #   userid = Column(Integer)
  #  storyid = Column(Integer)
   # time = Column(Integer)
