from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Table
from sqlalchemy.orm import relationship
from database import Base

package_tags = Table(
    'package_tags',
    Base.metadata,
    Column('package_id', Integer, ForeignKey('question_packages.package_id')),
    Column('tag_id', Integer, ForeignKey('tags.tag_id'))
)

class Role(Base):
    __tablename__ = 'roles'
    
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String, unique=True)
    
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String) 
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    
    role = relationship("Role", back_populates="users")
    question_packages = relationship("QuestionPackage", back_populates="user")

class Tag(Base):
    __tablename__ = 'tags'
    
    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String, unique=True)
    
    packages = relationship("QuestionPackage", secondary=package_tags, back_populates="tags")

class QuestionPackage(Base):
    __tablename__ = 'question_packages'
    
    package_id = Column(Integer, primary_key=True)
    package_name = Column(String)
    questions = Column(Text)  
    user_id = Column(Integer, ForeignKey('users.user_id'))
    
    user = relationship("User", back_populates="question_packages")
    tags = relationship("Tag", secondary=package_tags, back_populates="packages")