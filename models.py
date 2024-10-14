from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String, nullable=True)

    urls = relationship("URL", back_populates="user")

class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    long_url = Column(String, unique=True, nullable=False)
    short_url = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="urls")
