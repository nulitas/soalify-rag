from pydantic import BaseModel
from typing import List, Dict, Optional

class QACreate(BaseModel):
    question: str
    answer: str

class QAResponse(BaseModel):
    id: int
    package_id: int
    question: str
    answer: str

    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str
    fullname: str  
    role_id: int = 1

class UserResponse(BaseModel):
    user_id: int
    email: str
    fullname: str  
    role_id: int
    
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    fullname: Optional[str] = None
    role_id: Optional[int] = None

class TagCreate(BaseModel):
    tag_name: str

class TagResponse(BaseModel):
    tag_id: int
    tag_name: str
    user_id: int
    
    class Config:
        orm_mode = True

class PackageCreate(BaseModel):
    package_name: str
    questions: Optional[List[QACreate]] = []
    tag_ids: List[int] = []

class PackageResponse(BaseModel):
    id: int
    package_name: str
    questions: Optional[List["QAResponse"]] = []
    user_id: int
    tags: List[TagResponse] = []

    class Config:
        orm_mode = True

class QueryRequest(BaseModel):
    query_text: str
    num_questions: int = 1
    use_rag: bool = True