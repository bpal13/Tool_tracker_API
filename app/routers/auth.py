from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Optional
# from app.routers.post import router
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db


router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(response: Response, credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.Users).filter(models.Users.username == credentials.username).first()

    # Check if user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Verify password
    if not utils.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Create Access Token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # Create Refresh Token
    refresh_token = oauth2.create_refresh_token(data={"user_id": user.id})

    # Update 'last_login' field
    user.last_login = datetime.now(timezone.utc)
    db.commit()

    # Refresh Token sent as a cookie
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

    # Return JWT Token
    return {"access_token": access_token, "token_type": "bearer"}
    

# Get logged in user
@router.get('/me', response_model=schemas.UserOut)
def me(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    user = db.query(models.Users).filter(models.Users.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    return user


# Refresh the access token
@router.get('/refresh', response_model=schemas.Token)
def refresh(refresh_token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):

    print(refresh_token)
    data = oauth2.verify_refresh_token(token=refresh_token)

    #Check if user exist
    user = db.query(models.Users).filter(models.Users.id == data.id).first()
    if user: 
        new_access_token = oauth2.create_access_token({"user_id": data.id})
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found.')

    return {"access_token": new_access_token, "token_type": "bearer"}

  