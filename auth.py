from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
# from project.database import get_db
# from project.models import User


def get_current_user(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return user


