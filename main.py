import webbrowser
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from database import Base
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

security = HTTPBasic()

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


@app.get("/get_user")
def get_user(db: Session = Depends(get_db)):
    return db.query(models.User).id()


@app.get("/get_all_users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.delete("/delete_url", response_model=schemas.URLCreate)
def delete_url(short_url: str, db: Session = Depends(get_db)):
    url = crud.delete_url(db=db, short_url=short_url)
    return url


def verify_credentials(credentials: HTTPBasicCredentials, user: models.User):   # Verifica daca username si pass sunt ok
    print(credentials.username, credentials.password)
    if credentials.username != user.username or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return True


@app.get("/{short_link}", response_class=HTMLResponse)
async def get_login_form(short_link: str, credentials: HTTPBasicCredentials = Depends(security),
                         db: Session = Depends(get_db)):
    url_mapper = db.query(models.URL).where(models.URL.short_url == short_link).first()
    if url_mapper is None:
        raise HTTPException(
            status_code=404,
            detail=f"No URL found for short link: {short_link}",
        )
    user = db.query(models.User).where(models.User.id == url_mapper.user_id).first()
    print(url_mapper.long_url)
    if (verify_credentials(credentials, user) == True):
        # return RedirectResponse(url=url_mapper.long_url)
        # webbrowser.open(url_mapper.long_url, new=0, autoraise=True)
        return url_mapper.long_url


@app.get("/get_long_url")
def get_long_url(short_url: str, user_id: int, db: Session = Depends(get_db)):
    return crud.get_long_url(short_url, user_id, db)

#
# @app.get("/{short_url}")
# def get_long_url(short_url:str, db:Session = Depends(get_db)):
#     long_url = crud.get_long_url(short_url, user_id, db)
#     return ..... #(sau redirect)
