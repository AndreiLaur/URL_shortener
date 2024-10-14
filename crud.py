import webbrowser

from sqlalchemy.orm import Session
import models, schemas
from url_shortener_format import get_short_url


def create_user(db: Session, user: schemas.UserCreate):
    user_data = user.dict().copy()
    user_data.pop("id")
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_url(db: Session, url: schemas.URLCreate):
    user = db.query(models.User).where(models.User.id == url.user_id).first()
    if user is None:                                                        # verificam daca user-ul exista in BD
        return f"There is no user with id {url.user_id}"
    db_url = models.URL(long_url=url.long_url, short_url=get_short_url(url.long_url), user_id=url.user_id)
                                                                            #verificam daca short-ul exista deja
    url = db.query(models.URL).where(models.URL.short_url == db_url.short_url).first()
    if url is not None:
        return f"Short url already in database with id client: {url.user_id}"
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
    webbrowser.open(long_url.long_url, new=0, autoraise=True)       # pt a deschide URL-ul original direct in browser
    return long_url.long_url