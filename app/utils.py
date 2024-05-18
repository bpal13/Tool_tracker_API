import datetime
from passlib.context import CryptContext
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from datetime import datetime, timezone



# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



# Tool status check
def update_calibration_status(tool, calibration, db: Session = Depends(get_db)):
    '''Updates the 'status' and the 'valid until' fields of the selected tool.'''
    today = datetime.now()

    if calibration == None:
        tool.status = "Nincs kalibrálva"
        tool.valid_until = None
        db.commit()

    if calibration and calibration.next_calibration > today:
        tool.status = "Kalibrált"
        tool.valid_until = calibration.next_calibration
        db.commit()

    if calibration and calibration.next_calibration < today:
        tool.status = "Lejárt kalibrálás"
        tool.valid_until = calibration.next_calibration
        db.commit()

    if calibration and calibration.rating == "Selejt":
        tool.status = "Selejt"
        tool.valid_until = calibration.next_calibration
        db.commit()