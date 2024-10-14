from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from database import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create_user/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/create_url/", response_model=schemas.URLCreate | str)
def create_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    return crud.create_url(db=db, url=url)


# @app.get("/get_urls/", response_model=list[schemas.URLCreate])
# def read_urls(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     urls = crud.get_urls(db, skip=skip, limit=limit)
#     return urls


@app.get("/get_urls")
def get_all_urls(db: Session = Depends(get_db)):
    return db.query(models.URL).all()


@app.get("/get_all_users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.delete("/delete_url", response_model=schemas.URLCreate)
def delete_url(short_url: str, db: Session = Depends(get_db)):
    url = crud.delete_url(db=db, short_url=short_url)
    return url


@app.get("/get_long_url")
def get_long_url(short_url:str, user_id:int, db:Session = Depends(get_db)):
    return crud.get_long_url(short_url, user_id, db)