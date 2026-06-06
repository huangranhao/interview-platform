from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Resume, User
from app.routes.auth import get_current_user

router = APIRouter()


@router.get(
    "/",
    tags=["简历"],
    summary="获取用户简历列表"
)
async def get_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的简历列表
    """
    resumes = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).order_by(Resume.created_at.desc()).all()
    
    result = []
    for resume in resumes:
        result.append({
            "id": resume.id,
            "title": resume.title,
            "real_name": resume.real_name,
            "phone": resume.phone,
            "email": resume.email,
            "education": resume.education,
            "major": resume.major,
            "work_experience": resume.work_experience,
            "is_active": resume.is_active,
            "created_at": resume.created_at,
            "updated_at": resume.updated_at
        })
    
    return result


@router.get(
    "/{resume_id}",
    tags=["简历"],
    summary="获取简历详情"
)
async def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取指定简历的详细信息
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")
    
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限访问")
    
    return {
        "id": resume.id,
        "title": resume.title,
        "real_name": resume.real_name,
        "phone": resume.phone,
        "email": resume.email,
        "education": resume.education,
        "major": resume.major,
        "work_experience": resume.work_experience,
        "skills": resume.skills,
        "projects": resume.projects,
        "summary": resume.summary,
        "is_active": resume.is_active,
        "created_at": resume.created_at,
        "updated_at": resume.updated_at
    }


@router.post(
    "/",
    tags=["简历"],
    summary="创建新简历"
)
async def create_resume(
    resume_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建一份新简历
    
    - **title**: 简历标题
    - **real_name**: 真实姓名
    - **phone**: 手机号
    - **email**: 邮箱
    - **education**: 学历
    - **major**: 专业
    - **work_experience**: 工作经验（年）
    - **skills**: 技能（用逗号分隔）
    - **projects**: 项目经验
    - **summary**: 个人简介
    """
    resume = Resume(
        user_id=current_user.id,
        title=resume_data.get("title", "我的简历"),
        real_name=resume_data.get("real_name", ""),
        phone=resume_data.get("phone", ""),
        email=resume_data.get("email", ""),
        education=resume_data.get("education", ""),
        major=resume_data.get("major", ""),
        work_experience=resume_data.get("work_experience", 0),
        skills=resume_data.get("skills", ""),
        projects=resume_data.get("projects", ""),
        summary=resume_data.get("summary", "")
    )
    
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    return {"message": "简历创建成功", "resume_id": resume.id}


@router.put(
    "/{resume_id}",
    tags=["简历"],
    summary="更新简历"
)
async def update_resume(
    resume_id: int,
    resume_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新简历信息
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")
    
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限修改")
    
    if "title" in resume_data:
        resume.title = resume_data["title"]
    if "real_name" in resume_data:
        resume.real_name = resume_data["real_name"]
    if "phone" in resume_data:
        resume.phone = resume_data["phone"]
    if "email" in resume_data:
        resume.email = resume_data["email"]
    if "education" in resume_data:
        resume.education = resume_data["education"]
    if "major" in resume_data:
        resume.major = resume_data["major"]
    if "work_experience" in resume_data:
        resume.work_experience = resume_data["work_experience"]
    if "skills" in resume_data:
        resume.skills = resume_data["skills"]
    if "projects" in resume_data:
        resume.projects = resume_data["projects"]
    if "summary" in resume_data:
        resume.summary = resume_data["summary"]
    
    db.commit()
    db.refresh(resume)
    
    return {"message": "简历更新成功", "resume_id": resume.id}


@router.delete(
    "/{resume_id}",
    tags=["简历"],
    summary="删除简历"
)
async def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除指定简历
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")
    
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除")
    
    db.delete(resume)
    db.commit()
    
    return {"message": "简历已删除", "resume_id": resume_id}
