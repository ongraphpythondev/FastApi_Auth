from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

engine = create_engine("sqlite:///fastapi_auth.db")

# Create a DeclarativeMeta instance
Base = declarative_base()

# Define To Do class inheriting from Base
class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(200))
    age = Column(Integer)


class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(String(500))
    # user_id = Column(Integer, ForeignKey('User.id'))
    # user = relationship("User",backref="User") 





