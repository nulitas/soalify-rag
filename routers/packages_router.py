from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas
from auth import get_current_active_user

router = APIRouter(prefix="/packages", tags=["Packages"])

@router.post("/", response_model=schemas.PackageResponse)
async def create_package(
    package: schemas.PackageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_package = models.Package(
        package_name=package.package_name,
        user_id=current_user.user_id 
    )
    db.add(db_package)
    db.commit()
    db.refresh(db_package)

    # Handle tags
    if package.tag_ids:
        tags = db.query(models.Tag).filter(
            models.Tag.tag_id.in_(package.tag_ids),
            models.Tag.user_id == current_user.user_id 
        ).all()
        db_package.tags = tags
    
    # Handle questions
    if package.questions:
        db_questions = [
            models.QA(
                package_id=db_package.id,
                question=q.question,
                answer=q.answer
            ) for q in package.questions
        ]
        db.add_all(db_questions)

    db.commit()
    db.refresh(db_package)
    return db_package

@router.get("/", response_model=List[schemas.PackageResponse])
async def get_packages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    packages = db.query(models.Package).filter(
        models.Package.user_id == current_user.user_id
    ).offset(skip).limit(limit).all()
    return packages

@router.get("/{package_id}", response_model=schemas.PackageResponse)
async def get_package(
    package_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_package = db.query(models.Package).filter(
        models.Package.id == package_id,
        models.Package.user_id == current_user.user_id 
    ).first()
    
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")

    return db_package

@router.put("/{package_id}", response_model=schemas.PackageResponse)
async def update_package(
    package_id: int,
    package: schemas.PackageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_package = db.query(models.Package).filter(
        models.Package.id == package_id,
        models.Package.user_id == current_user.user_id
    ).first()
    
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")

    db_package.package_name = package.package_name

    # Update tags (verify ownership)
    if package.tag_ids:
        tags = db.query(models.Tag).filter(
            models.Tag.tag_id.in_(package.tag_ids),
            models.Tag.user_id == current_user.user_id
        ).all()
        db_package.tags = tags
    else:
        db_package.tags.clear()

    # Update questions
    db.query(models.QA).filter(models.QA.package_id == package_id).delete()
    if package.questions:
        db_questions = [
            models.QA(package_id=package_id, question=q.question, answer=q.answer)
            for q in package.questions
        ]
        db.add_all(db_questions)

    db.commit()
    db.refresh(db_package)
    return db_package

@router.delete("/{package_id}")
async def delete_package(
    package_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_package = db.query(models.Package).filter(
        models.Package.id == package_id,
        models.Package.user_id == current_user.user_id
    ).first()
    
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")

    db.query(models.QA).filter(models.QA.package_id == package_id).delete()
    db.delete(db_package)
    db.commit()

    return {"detail": "Package deleted successfully"}