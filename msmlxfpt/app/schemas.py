from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Union
from datetime import datetime
from enum import Enum
import json

# 自定义JSON编码器，处理枚举类型
class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)

# 用户相关
class UserCreate(BaseModel):
    phone: str
    email: Optional[EmailStr] = None
    password: str
    nickname: Optional[str] = None
    role: Optional[str] = "user"

class UserLogin(BaseModel):
    username: str  # 手机号或邮箱
    password: str

class UserResponse(BaseModel):
    id: int
    phone: str
    email: Optional[str] = None
    nickname: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str

# 题目相关
class QuestionCreate(BaseModel):
    job_type: str
    difficulty: str
    content: str
    answer: str
    keywords: Optional[str] = ""

class QuestionResponse(BaseModel):
    id: int
    job_type: str
    difficulty: str
    content: str
    answer: Optional[str] = None
    keywords: str
    created_at: datetime
    
    class Config:
        orm_mode = True
        json_encoders = {
            Enum: lambda v: v.value
        }

class QuestionSearch(BaseModel):
    keyword: Optional[str] = None
    job_type: Optional[str] = None
    difficulty: Optional[str] = None

# 面试相关
class InterviewCreate(BaseModel):
    job_type: str
    difficulty: str
    duration: Optional[int] = 300  # 默认5分钟

class InterviewResponse(BaseModel):
    id: int
    user_id: int
    job_type: str
    difficulty: str
    status: str
    duration: int
    video_url: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        json_encoders = {
            Enum: lambda v: v.value
        }

class InterviewQuestionResponse(BaseModel):
    id: int
    question_id: int
    content: str
    order_num: int
    user_answer: Optional[str] = None
    answer_time: Optional[int] = None
    
    class Config:
        orm_mode = True

# 评估相关
class AssessmentResponse(BaseModel):
    id: int
    interview_id: int
    user_id: int
    overall_score: float
    content_score: float
    fluency_score: float
    confidence_score: float
    suggestions: str
    report: str
    created_at: datetime
    
    class Config:
        orm_mode = True

# 学习资源相关
class LearningResourceCreate(BaseModel):
    title: str
    content: str
    resource_type: str
    job_type: Optional[str] = "other"
    difficulty: Optional[str] = "junior"

class LearningResourceResponse(BaseModel):
    id: int
    title: str
    content: str
    resource_type: str
    job_type: str
    difficulty: str
    view_count: int
    created_at: datetime
    
    class Config:
        orm_mode = True
        json_encoders = {
            Enum: lambda v: v.value
        }

class LearningRecordCreate(BaseModel):
    resource_id: int
    progress: float = 0.0
    completed: bool = False

class LearningRecordResponse(BaseModel):
    id: int
    user_id: int
    resource_id: int
    progress: float
    completed: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

# 企业相关
class EnterpriseCreate(BaseModel):
    name: str
    industry: Optional[str] = None
    scale: Optional[str] = None
    description: Optional[str] = None

class EnterpriseResponse(BaseModel):
    id: int
    user_id: int
    name: str
    industry: Optional[str] = None
    scale: Optional[str] = None
    description: Optional[str] = None
    is_verified: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class CustomQuestionCreate(BaseModel):
    content: str
    answer: Optional[str] = None
    difficulty: str = "middle"

class CustomQuestionResponse(BaseModel):
    id: int
    enterprise_id: int
    content: str
    answer: Optional[str] = None
    difficulty: str
    created_at: datetime
    
    class Config:
        orm_mode = True
        json_encoders = {
            Enum: lambda v: v.value
        }

class EnterpriseCandidateResponse(BaseModel):
    id: int
    enterprise_id: int
    user_id: int
    status: str
    score: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True
