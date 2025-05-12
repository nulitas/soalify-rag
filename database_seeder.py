from sqlalchemy.orm import Session
import models
from typing import List

def seed_roles(db: Session) -> None:
    """
    Seeds the database with default roles if they don't already exist.
    
    Args:
        db: SQLAlchemy database session
    """

    default_roles = [
        {"role_name": "Admin"},
        {"role_name": "User"},
    ]
    
    for role_data in default_roles:
        existing_role = db.query(models.Role).filter(
            models.Role.role_name == role_data["role_name"]
        ).first()
        
        if not existing_role:
            new_role = models.Role(**role_data)
            db.add(new_role)
            print(f"Created role: {role_data['role_name']}")
    
    db.commit()
    
def seed_admin_user(db: Session, admin_email: str, admin_password: str) -> None:
    """
    Seeds the database with a default admin user if it doesn't already exist.
    
    Args:
        db: SQLAlchemy database session
        admin_email: Email for the admin user
        admin_password: Password for the admin user
    """
    from auth import get_password_hash
    
    admin_role = db.query(models.Role).filter(models.Role.role_name == "admin").first()
    
    if not admin_role:
        raise ValueError("Admin role not found. Please run seed_roles first.")
    
    existing_admin = db.query(models.User).filter(models.User.email == admin_email).first()
    
    if not existing_admin:
        hashed_password = get_password_hash(admin_password)
        admin_user = models.User(
            email=admin_email,
            password=hashed_password,
            fullname="System Administrator",
            role_id=admin_role.role_id
        )
        db.add(admin_user)
        db.commit()
        print(f"Created admin user: {admin_email}")
    else:
        print(f"Admin user already exists: {admin_email}")

def seed_database(db: Session) -> None:
    """
    Main function to seed the database with initial data.
    
    Args:
        db: SQLAlchemy database session
    """
    seed_roles(db)
    
    print("Database seeding completed!")