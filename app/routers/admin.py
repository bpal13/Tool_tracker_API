from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..database import get_db



router = APIRouter(
    prefix="/admin",
    tags=["Administrator"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password
    password_hash = utils.hash(user.password)
    user.password = password_hash

    # Add new user
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()

    return new_user


# Delete a Tool
@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tool(id: int, db: Session = Depends(get_db)):
    pass