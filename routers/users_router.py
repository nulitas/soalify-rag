from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext 
from database import get_db
import models
import schemas
from datetime import timedelta

from auth import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    get_current_active_user
)

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def is_admin(user: models.User) -> bool:
    """Check if the user has admin role (role_id=1)"""
    return user.role_id == 1

def admin_required(current_user: models.User = Depends(get_current_active_user)):
    """Dependency to check if the current user is an admin"""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required for this operation"
        )
    return current_user

@router.post("/register", response_model=schemas.UserResponse)
async def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can register new users"
        )
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, 
        password=hashed_password, 
        fullname=user.fullname,  
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/public/register", response_model=schemas.UserResponse)
async def public_register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_role_id = 2
    
    db_user = models.User(
        email=user.email, 
        password=hashed_password, 
        fullname=user.fullname,  
        role_id=user_role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=timedelta(minutes=30)
    )
    
    user_data = {  
        "user_id": user.user_id,
        "email": user.email,
        "fullname": user.fullname,
        "role_id": user.role_id,
        "is_admin": is_admin(user)
    }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_data
    }

@router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(
    current_user: models.User = Depends(get_current_active_user)
):
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "fullname": current_user.fullname,
        "role_id": current_user.role_id,
        "is_admin": is_admin(current_user)
    }

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if not is_admin(current_user) and current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user's information"
        )
    
    db_user = db.query(models.User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = {
        "user_id": db_user.user_id,
        "email": db_user.email,
        "fullname": db_user.fullname,
        "role_id": db_user.role_id,
        "is_admin": is_admin(db_user)
    }
    return result

@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: int, 
    user_update: schemas.UserUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if current_user.user_id != user_id and not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to update this user"
        )
    
    db_user = db.query(models.User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.role_id is not None and not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can change user roles"
        )
    
    if user_update.email is not None:
        existing_user = db.query(models.User).filter(
            models.User.email == user_update.email,
            models.User.user_id != user_id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        db_user.email = user_update.email
    
    if user_update.fullname is not None:
        db_user.fullname = user_update.fullname
    if user_update.role_id is not None:
        db_user.role_id = user_update.role_id
    if user_update.password is not None:
        db_user.password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(db_user)
    
    result = {
        "user_id": db_user.user_id,
        "email": db_user.email,
        "fullname": db_user.fullname,
        "role_id": db_user.role_id,
        "is_admin": is_admin(db_user)
    }
    return result

@router.put("/{user_id}/password")
async def update_password(
    user_id: int,
    password_update: schemas.PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):

    if user_id != current_user.user_id and not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own password"
        )
    
    db_user = db.query(models.User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_id == current_user.user_id or not is_admin(current_user):

        if not verify_password(password_update.current_password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
    
    hashed_password = get_password_hash(password_update.new_password)
    db_user.password = hashed_password
    db.commit()
    
    return {"message": "Password updated successfully"}

@router.delete("/{user_id}")
async def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    
    if not is_admin(current_user) and current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )
    
    db_user = db.query(models.User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if is_admin(db_user):
        admin_count = db.query(models.User).filter(models.User.role_id == 1).count()
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete the last admin account"
            )
    
    try:
        db.delete(db_user)
        db.commit()
        
        return {"message": "User and all related data deleted successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )

@router.get("/", response_model=List[schemas.UserResponse])
async def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to view all users"
        )
    
    users = db.query(models.User).offset(skip).limit(limit).all()
    result = []
    for user in users:
        result.append({
            "user_id": user.user_id,
            "email": user.email,
            "fullname": user.fullname,
            "role_id": user.role_id,
            "is_admin": is_admin(user)
        })
    return result

@router.get("/roles/")
async def get_roles(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    roles = db.query(models.Role).all()
    return [{
        "role_id": int(role.role_id),  
        "role_name": role.role_name
    } for role in roles]