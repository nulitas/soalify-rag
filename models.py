from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Role(Base):
    __tablename__ = 'roles'
    
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String, unique=True)
    
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)  
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    
    role = relationship("Role", back_populates="users")