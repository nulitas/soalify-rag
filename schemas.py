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
    is_admin: Optional[bool] = None  
    is_seeded: Optional[bool] = False
    
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    fullname: Optional[str] = None
    role_id: Optional[int] = None

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None

class TagCreate(BaseModel):
    tag_name: str

class TagUpdate(BaseModel):
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
    selected_documents: Optional[List[str]] = None
    target_learning_outcome: Optional[str] = None 
    
    class Config:
        json_schema_extra = {
            "example": {
                "query_text": "Machine learning concepts",
                "num_questions": 3,
                "use_rag": True,
                "selected_documents": ["document1.pdf", "document2.pdf"],
                "target_learning_outcome": "Pemahaman konseptual"
            }
        }