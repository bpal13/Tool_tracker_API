from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db



router = APIRouter(
    prefix="/admin",
    tags=["Administrator"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut,)
# def register(user: schemas.UserCreate, db: Session = Depends(get_db), authorize: bool = Depends(oauth2.CheckRoles(['admin']))):  
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):  


    # Check for existing username and employee ID
    validate_username = db.query(models.Users).filter(models.Users.username == user.username).first()
    if validate_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exist.")

    validate_employee_id = db.query(models.Users).filter(models.Users.employee_id == user.employee_id).first()
    if validate_employee_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee ID already exist.")


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


# Testing
@router.get("/get-user")
def get_user(db: Session = Depends(get_db), authorize: bool = Depends(oauth2.CheckRoles(['admin']))):

    user = db.query(models.Users).filter(models.Users.id == 3).first()

    return {"message": "success"}