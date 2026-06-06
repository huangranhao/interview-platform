from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base

# 用户角色枚举
class UserRole(PyEnum):
    USER = "user"
    ENTERPRISE = "enterprise"
    ADMIN = "admin"

# 面试难度枚举
class InterviewDifficulty(PyEnum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"

# 岗位类型枚举
class JobType(PyEnum):
    TECH = "tech"
    PRODUCT = "product"
    OPERATION = "operation"
    DESIGN = "design"
    OTHER = "other"

# 用户模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    nickname = Column(String(50))
    avatar = Column(String(255))
    role = Column(SQLEnum(UserRole, values_callable=lambda x: [e.value for e in x]), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now, index=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, index=True)
    
    # 关系
    interviews = relationship("Interview", back_populates="user")
    favorites = relationship("FavoriteQuestion", back_populates="user")
    learning_records = relationship("LearningRecord", back_populates="user")
    assessments = relationship("Assessment", back_populates="user")

# 企业用户模型
class Enterprise(Base):
    __tablename__ = "enterprises"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100))
    industry = Column(String(50))
    scale = Column(String(20))
    description = Column(Text)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    user = relationship("User", backref="enterprise")
    custom_questions = relationship("CustomQuestion", back_populates="enterprise")
    candidates = relationship("EnterpriseCandidate", back_populates="enterprise")

# 面试模型
class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    job_type = Column(SQLEnum(JobType, values_callable=lambda x: [e.value for e in x]), index=True)
    difficulty = Column(SQLEnum(InterviewDifficulty, values_callable=lambda x: [e.value for e in x]), index=True)
    status = Column(String(20), default="in_progress", index=True)
    video_url = Column(String(255))
    duration = Column(Integer, default=300)
    created_at = Column(DateTime, default=datetime.now, index=True)
    completed_at = Column(DateTime, index=True)
    
    # 关系
    user = relationship("User", back_populates="interviews")
    questions = relationship("InterviewQuestion", back_populates="interview")
    assessment = relationship("Assessment", back_populates="interview", uselist=False)

# 题目模型
class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(SQLEnum(JobType, values_callable=lambda x: [e.value for e in x]), index=True)
    difficulty = Column(SQLEnum(InterviewDifficulty, values_callable=lambda x: [e.value for e in x]), index=True)
    content = Column(Text)
    answer = Column(Text)
    keywords = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.now, index=True)
    
    # 关系
    interviews = relationship("InterviewQuestion", back_populates="question")
    favorites = relationship("FavoriteQuestion", back_populates="question")

# 面试题目关联模型
class InterviewQuestion(Base):
    __tablename__ = "interview_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), index=True)
    order_num = Column(Integer, index=True)
    user_answer = Column(Text)
    answer_time = Column(Integer)
    
    # 关系
    interview = relationship("Interview", back_populates="questions")
    question = relationship("Question", back_populates="interviews")

# 评估模型
class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    overall_score = Column(Float)
    content_score = Column(Float)
    fluency_score = Column(Float)
    confidence_score = Column(Float)
    suggestions = Column(Text)
    report = Column(Text)
    created_at = Column(DateTime, default=datetime.now, index=True)
    
    # 关系
    interview = relationship("Interview", back_populates="assessment")
    user = relationship("User", back_populates="assessments")

# 学习资源模型
class LearningResource(Base):
    __tablename__ = "learning_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text)
    resource_type = Column(String(20))
    job_type = Column(SQLEnum(JobType, values_callable=lambda x: [e.value for e in x]))
    difficulty = Column(SQLEnum(InterviewDifficulty, values_callable=lambda x: [e.value for e in x]))
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    learning_records = relationship("LearningRecord", back_populates="resource")

# 学习记录模型
class LearningRecord(Base):
    __tablename__ = "learning_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resource_id = Column(Integer, ForeignKey("learning_resources.id"))
    progress = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    user = relationship("User", back_populates="learning_records")
    resource = relationship("LearningResource", back_populates="learning_records")

# 简历模型
class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    title = Column(String(100))
    real_name = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    education = Column(String(100))
    major = Column(String(100))
    work_experience = Column(Integer)
    skills = Column(Text)
    projects = Column(Text)
    summary = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.now, index=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, index=True)
    
    # 关系
    user = relationship("User", back_populates="resumes")

# 更新User模型关系
User.resumes = relationship("Resume", back_populates="user")

# 收藏题目模型
class FavoriteQuestion(Base):
    __tablename__ = "favorite_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    user = relationship("User", back_populates="favorites")
    question = relationship("Question", back_populates="favorites")

# 企业自定义题目模型
class CustomQuestion(Base):
    __tablename__ = "custom_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    enterprise_id = Column(Integer, ForeignKey("enterprises.id"))
    content = Column(Text)
    answer = Column(Text)
    difficulty = Column(SQLEnum(InterviewDifficulty, values_callable=lambda x: [e.value for e in x]))
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    enterprise = relationship("Enterprise", back_populates="custom_questions")

# 企业候选人模型
class EnterpriseCandidate(Base):
    __tablename__ = "enterprise_candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    enterprise_id = Column(Integer, ForeignKey("enterprises.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(20), default="pending")
    score = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    enterprise = relationship("Enterprise", back_populates="candidates")
    user = relationship("User", backref="enterprise_candidates")
