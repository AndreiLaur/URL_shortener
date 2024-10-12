from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_url(db: Session, url: schemas.URLCreate, user_id: int):
    db_url = models.URL(long=url.long, short=url.short, user_id=user_id)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_urls(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.URL).offset(skip).limit(limit).all()

def get_url_by_short(db: Session, short_url: str):
    return db.query(models.URL).filter(models.URL.short == short_url).first()

def delete_url(db: Session, short_url: str):
    db_url = get_url_by_short(db, short_url)
    if db_url:
        db.delete(db_url)
        db.commit()
    return db_url
