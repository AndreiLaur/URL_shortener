from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from database import get_db
from models import User
import bcrypt


def authenticate_user(credentials: HTTPBasicCredentials, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not bcrypt.checkpw(credentials.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
