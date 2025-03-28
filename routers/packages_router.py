from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/packages", tags=["Packages"])

@router.post("/", response_model=schemas.PackageResponse)
async def create_package(package: schemas.PackageCreate, db: Session = Depends(get_db), user_id: int = 1):
    db_package = models.QuestionPackage(
        package_name=package.package_name,
        questions=package.questions,
        user_id=user_id
    )
    
    if package.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.tag_id.in_(package.tag_ids)).all()
        db_package.tags = tags
    
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package

@router.get("/", response_model=List[schemas.PackageResponse])
async def get_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    packages = db.query(models.QuestionPackage).offset(skip).limit(limit).all()
    return packages

@router.get("/{package_id}", response_model=schemas.PackageResponse)
async def get_package(package_id: int, db: Session = Depends(get_db)):
    db_package = db.query(models.QuestionPackage).filter(models.QuestionPackage.package_id == package_id).first()
    if db_package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return db_package

@router.put("/{package_id}", response_model=schemas.PackageResponse)
async def update_package(
    package_id: int,
    package: schemas.PackageCreate,
    db: Session = Depends(get_db)
):
    db_package = db.query(models.QuestionPackage).filter(models.QuestionPackage.package_id == package_id).first()
    if db_package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    
    db_package.package_name = package.package_name
    if package.questions is not None:
        db_package.questions = package.questions

    if package.tag_ids is not None:
        db_package.tags.clear()
        
        if package.tag_ids:
            tags = db.query(models.Tag).filter(models.Tag.tag_id.in_(package.tag_ids)).all()
            db_package.tags = tags
    
    db.commit()
    db.refresh(db_package)
    return db_package

@router.delete("/{package_id}")
async def delete_package(package_id: int, db: Session = Depends(get_db)):
    db_package = db.query(models.QuestionPackage).filter(models.QuestionPackage.package_id == package_id).first()
    if db_package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    
    db.delete(db_package)
    db.commit()
    return {"detail": "Package deleted successfully"}