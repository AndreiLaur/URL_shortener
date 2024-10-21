from sqlalchemy.orm import Session
from . import models, schemas
import bcrypt

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db_user.password = get_password_hash(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_url(db: Session, url: schemas.URLCreate):
    db_url = models.URL(**url.dict())
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_url(db: Session, url_id: int):
    return db.query(models.URL).filter(models.URL.id == url_id).first()

def delete_url(db: Session, url_id: int):
    url = db.query(models.URL).filter(models.URL.id == url_id).first()
    if url:
        db.delete(url)
        db.commit()
    return url
