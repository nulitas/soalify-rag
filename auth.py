import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    import secrets
    SECRET_KEY = secrets.token_hex(32)
    print(f"WARNING: Generated a new SECRET_KEY. Store this in your environment!")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt"], 
    bcrypt__default_rounds=12,
    bcrypt__min_rounds=4,
    bcrypt__max_rounds=31,
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})

    to_encode.update({
        "iat": datetime.utcnow(),  
        "nbf": datetime.utcnow(),  
    })
    
    # print(f"Creating token with payload: {to_encode}") 
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # print(f"Received token: {token}") 

        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        
        # print(f"Decoded payload: {payload}")
        
        email: str = payload.get("sub")
        if email is None:
            print("No email (sub) in token payload")
            raise credentials_exception
        
        token_data = schemas.TokenData(email=email)
    except JWTError as e:
        print(f"JWT Decode Error: {str(e)}")
        print(f"Token: {token}")
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        print(f"No user found with email: {token_data.email}")
        raise credentials_exception
    
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    return current_user