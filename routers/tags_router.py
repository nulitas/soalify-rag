from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("/", response_model=schemas.TagResponse)
async def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db), user_id: int = 1):
    db_tag = db.query(models.Tag).filter(models.Tag.tag_name == tag.tag_name).first()
    if db_tag:
        raise HTTPException(status_code=400, detail="Tag already exists")
    db_tag = models.Tag(tag_name=tag.tag_name, user_id=user_id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@router.get("/", response_model=List[schemas.TagResponse])
async def get_tags(
    user_id: int = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Tag)
    if user_id is not None:
        query = query.filter(models.Tag.user_id == user_id)
    tags = query.offset(skip).limit(limit).all()
    return tags

@router.delete("/{tag_id}", response_model=schemas.TagResponse)
async def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(models.Tag).filter(models.Tag.tag_id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
    return tag

