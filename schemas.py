from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    email: str
    password: str
    role_id: int = 1  

class UserResponse(BaseModel):
    user_id: int
    email: str
    role_id: int
    
    class Config:
        orm_mode = True

class TagCreate(BaseModel):
    tag_name: str

class TagResponse(BaseModel):
    tag_id: int
    tag_name: str
    
    class Config:
        orm_mode = True

class PackageCreate(BaseModel):
    package_name: str
    questions: Optional[str] = None
    tag_ids: List[int] = []

class PackageResponse(BaseModel):
    package_id: int
    package_name: str
    questions: Optional[str] = None
    user_id: int
    tags: List[TagResponse] = []
    
    class Config:
        orm_mode = True

class QueryRequest(BaseModel):
    query_text: str
    num_questions: int = 1
    use_rag: bool = True