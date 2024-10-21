from fastapi import FastAPI, Depends, HTTPException
import webbrowser
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine, get_db
from database import Base
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from auth import authenticate_user

app = FastAPI()
security = HTTPBasic()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/Create_User/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Endpoint for users to create a new account (no authentication needed)."""
    return crud.create_user(db=db, user=user)


@app.post("/Create_URL/", response_model=schemas.URLCreate)
def create_url(url: schemas.URLCreate, credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    """Endpoint to create a new URL, requires authentication."""
    user = authenticate_user(credentials, db)
    url.user_id = user.id
    return crud.create_url(db=db, url=url)


@app.get("/Get_URLs/", response_model=list[schemas.URLCreate])
def get_urls(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    """Endpoint to get all URLs for the authenticated user, requires authentication."""
    user = authenticate_user(credentials, db)
    urls = db.query(models.URL).filter(models.URL.user_id == user.id).all()
    return urls


@app.get("/Get_User/", response_model=schemas.User)
def get_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    """Endpoint to get a specific user, requires authentication."""
    user = authenticate_user(credentials, db)
    return user


@app.get("/Get_All_Users_For_Info")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.delete("/Delete_URL/", response_model=schemas.URLCreate)
def delete_url(short_url: str, credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    """Endpoint to delete a URL, requires authentication."""
    user = authenticate_user(credentials, db)
    db_url = db.query(models.URL).filter(models.URL.short_url == short_url, models.URL.user_id == user.id).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found or not owned by the user.")
    db.delete(db_url)
    db.commit()
    return db_url


def verify_credentials(credentials: HTTPBasicCredentials, user: models.User):
    print(credentials.username, credentials.password)
    if credentials.username != user.username or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return True


@app.get("/Short_URL_to_Long_URL/{short_link}")
def get_long_url(short_link: str, credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    """Return the long URL corresponding to the provided short link, requires authentication."""
    user = authenticate_user(credentials, db)
    long_url_entry = db.query(models.URL).filter(models.URL.short_url == short_link,
                                                 models.URL.user_id == user.id).first()
    if long_url_entry is None:
        raise HTTPException(status_code=404, detail="No URL found for short link or not owned by user.")
    return long_url_entry.long_url


from fastapi.responses import RedirectResponse


@app.get("/{short_url_after_IP}", response_class=RedirectResponse)
def redirect_to_long_url(short_url_after_IP: str, db: Session = Depends(get_db)):
    """Redirect the short URL to the corresponding long URL."""
    # Fetch the long URL associated with the short URL
    long_url_entry = crud.get_url_by_short(db, short_url_after_IP)

    # If the short URL doesn't exist, return a 404 error
    if long_url_entry is None:
        raise HTTPException(status_code=404, detail="URL not found.")

    # Redirect to the long URL
    return RedirectResponse(url=long_url_entry.long_url)

