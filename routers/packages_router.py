from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/packages", tags=["Packages"])

@router.post("/", response_model=schemas.PackageResponse)
async def create_package(package: schemas.PackageCreate, db: Session = Depends(get_db), user_id: int = 1):
    db_package = models.Package(
        package_name=package.package_name,
        user_id=user_id
    )
    db.add(db_package)
    db.commit()
    db.refresh(db_package)

    if package.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.tag_id.in_(package.tag_ids)).all()
        db_package.tags = tags 
    
    if package.questions:
        db_questions = [
            models.QA(package_id=db_package.id, question=q.question, answer=q.answer)
            for q in package.questions
        ]
        db.add_all(db_questions)

    db.commit()
    db.refresh(db_package)

    return db_package

@router.get("/", response_model=List[schemas.PackageResponse])
async def get_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    packages = db.query(models.Package).offset(skip).limit(limit).all()
    return packages

@router.get("/{package_id}", response_model=schemas.PackageResponse)
async def get_package(package_id: int, db: Session = Depends(get_db)):
    db_package = db.query(models.Package).filter(models.Package.id == package_id).first()
    if db_package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    questions = db.query(models.QA).filter(models.QA.package_id == package_id).all()
    db_package.questions = questions  

    return db_package

@router.put("/{package_id}", response_model=schemas.PackageResponse)
async def update_package(
    package_id: int,
    package: schemas.PackageCreate,
    db: Session = Depends(get_db)
):
    db_package = db.query(models.Package).filter(models.Package.id == package_id).first()
    if db_package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    db_package.package_name = package.package_name

    if package.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.tag_id.in_(package.tag_ids)).all()
        db_package.tags = tags
    else:
        db_package.tags.clear()

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
async def delete_package(package_id: int, db: Session = Depends(get_db)):
    db_package = db.query(models.Package).filter(models.Package.id == package_id).first() 
    if db_package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    db.query(models.QA).filter(models.QA.package_id == package_id).delete()

    db.delete(db_package)
    db.commit()

    return {"detail": "Package deleted successfully"}
