from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from projectx import crud, models, schemas
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/urls/", response_model=schemas.URLCreate)
def create_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    return crud.create_url(db=db, url=url)

@app.get("/urls/", response_model=list[schemas.URLCreate])
def read_urls(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    urls = crud.get_urls(db, skip=skip, limit=limit)
    return urls

@app.delete("/urls/{short_url}", response_model=schemas.URLCreate)
def delete_url(short_url: str, db: Session = Depends(get_db)):
    url = crud.delete_url(db=db, short_url=short_url)
    return url
