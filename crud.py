import webbrowser
from http.client import HTTPException

from sqlalchemy.orm import Session
import models, schemas
from url_shortener_format import get_short_url
import bcrypt


def create_user(db: Session, user: schemas.UserCreate):
    user_data = user.dict().copy()
    user_data.pop("id")
    hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
    user_data['password'] = hashed_password.decode('utf-8')
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_url(db: Session, url: schemas.URLCreate):
    user = db.query(models.User).filter(models.User.id == url.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"There is no user with id {url.user_id}")

    existing_url = db.query(models.URL).filter(models.URL.short_url == url.short_url).first()
    if existing_url is not None:
        raise HTTPException(status_code=400, detail="Short URL already exists in the database.")

    db_url = models.URL(long_url=url.long_url, short_url=get_short_url(url.long_url), user_id=url.user_id)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_urls(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.URL).offset(skip).limit(limit).all()


def get_url_by_short(db: Session, short_url: str):
    return db.query(models.URL).filter(models.URL.short_url == short_url).first()


def delete_url(db: Session, short_url: str):
    db_url = get_url_by_short(db, short_url)
    if db_url:
        db.delete(db_url)
        db.commit()
    return db_url


def get_long_url(requested_short_url:str, requested_user_id:int, db:Session):
    long_url = db.query(models.URL).where(models.URL.user_id == requested_user_id, models.URL.short_url == requested_short_url).first()
    if long_url is None:
        return f"there is no long url associated to this short url : '{requested_short_url}' or user_id: {requested_user_id}"
    return long_url.long_url