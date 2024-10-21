from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    urls = relationship("URL", back_populates="owner")

class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    long_url = Column(String, unique=True, nullable=False)
    short_url = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="urls")
