from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from database import Base

package_tags = Table(
    "package_tags",
    Base.metadata,
    Column("package_id", Integer, ForeignKey("packages.id")),
    Column("tag_id", Integer, ForeignKey("tags.tag_id"))
)

class Role(Base):
    __tablename__ = "roles"
    
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String, unique=True)
    
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String) 
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    
    role = relationship("Role", back_populates="users")
    packages = relationship("Package", back_populates="user")
    tags = relationship("Tag", back_populates="user")

class Tag(Base):
    __tablename__ = "tags"
    
    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    
    user = relationship("User", back_populates="tags")
    packages = relationship("Package", secondary=package_tags, back_populates="tags")

class Package(Base):
    __tablename__ = "packages"
    
    id = Column(Integer, primary_key=True)
    package_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    
    user = relationship("User", back_populates="packages")
    tags = relationship("Tag", secondary=package_tags, back_populates="packages")
    questions = relationship("QA", back_populates="package", cascade="all, delete-orphan")

class QA(Base):
    __tablename__ = "qa"
    
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey("packages.id"))  
    question = Column(Text)
    answer = Column(Text)

    package = relationship("Package", back_populates="questions")
