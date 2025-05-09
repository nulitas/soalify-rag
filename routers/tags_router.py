from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas
from auth import get_current_active_user  

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("/", response_model=schemas.TagResponse)
async def create_tag(
    tag: schemas.TagCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user) 
):
    db_tag = db.query(models.Tag).filter(
        models.Tag.tag_name == tag.tag_name,
        models.Tag.user_id == current_user.user_id  
    ).first()
    
    if db_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag already exists for your account"
        )
        
    db_tag = models.Tag(
        tag_name=tag.tag_name,
        user_id=current_user.user_id 
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@router.get("/", response_model=List[schemas.TagResponse])
async def get_tags(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user) 
):
    return db.query(models.Tag).filter(
        models.Tag.user_id == current_user.user_id
    ).all()


@router.put("/{tag_id}", response_model=schemas.TagResponse)
async def update_tag(
    tag_id: int,
    tag_update: schemas.TagUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):

    tag = db.query(models.Tag).filter(
        models.Tag.tag_id == tag_id,
        models.Tag.user_id == current_user.user_id
    ).first()
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found or not owned by you"
        )
    
    existing_tag = db.query(models.Tag).filter(
        models.Tag.tag_name == tag_update.tag_name,
        models.Tag.user_id == current_user.user_id,
        models.Tag.tag_id != tag_id
    ).first()
    
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag name already exists for your account"
        )
    
    tag.tag_name = tag_update.tag_name
    db.commit()
    db.refresh(tag)
    return tag

@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user) 
):
    tag = db.query(models.Tag).filter(
        models.Tag.tag_id == tag_id,
        models.Tag.user_id == current_user.user_id  
    ).first()
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found or not owned by you"
        )
    
    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted successfully"}