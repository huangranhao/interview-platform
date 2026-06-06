from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import User, Interview, Assessment
from app.schemas import UserResponse
from app.routes.auth import get_current_user
from app.utils import get_password_hash, verify_password

router = APIRouter()

@router.get(
    "/",
    response_model=UserResponse,
    tags=["个人中心"],
    summary="获取个人信息"
)
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户的个人信息
    """
    return current_user

@router.put(
    "/",
    response_model=UserResponse,
    tags=["个人中心"],
    summary="更新个人信息"
)
async def update_profile(
    nickname: Optional[str] = None,
    avatar: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新当前用户的个人信息

    - **nickname**: 昵称（可选）
    - **avatar**: 头像URL（可选）
    """
    if nickname:
        current_user.nickname = nickname
    if avatar:
        current_user.avatar = avatar

    db.commit()
    db.refresh(current_user)

    return current_user

@router.put(
    "/password",
    tags=["个人中心"],
    summary="修改密码"
)
async def update_password(
    old_password: str = Query(..., description="旧密码"),
    new_password: str = Query(..., description="新密码"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    修改当前用户的登录密码

    - **old_password**: 旧密码
    - **new_password**: 新密码
    """
    if not verify_password(old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="旧密码错误")

    current_user.password_hash = get_password_hash(new_password)
    db.commit()

    return {"message": "密码修改成功"}

@router.get(
    "/interviews",
    tags=["个人中心"],
    summary="获取我的面试记录"
)
async def get_my_interviews(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的面试历史记录

    - **page**: 页码
    - **size**: 每页数量
    """
    interviews = db.query(Interview).filter(
        Interview.user_id == current_user.id
    ).order_by(Interview.created_at.desc()).offset((page - 1) * size).limit(size).all()

    result = []
    for interview in interviews:
        assessment = db.query(Assessment).filter(Assessment.interview_id == interview.id).first()

        result.append({
            "id": interview.id,
            "job_type": interview.job_type.value,
            "difficulty": interview.difficulty.value,
            "status": interview.status,
            "created_at": interview.created_at,
            "completed_at": interview.completed_at,
            "overall_score": assessment.overall_score if assessment else None
        })

    return result

@router.get(
    "/assessments",
    tags=["个人中心"],
    summary="获取我的评估报告"
)
async def get_my_assessments(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的所有评估报告

    - **page**: 页码
    - **size**: 每页数量
    """
    assessments = db.query(Assessment).filter(
        Assessment.user_id == current_user.id
    ).order_by(Assessment.created_at.desc()).offset((page - 1) * size).limit(size).all()

    return assessments

@router.get(
    "/stats",
    tags=["个人中心"],
    summary="获取个人统计数据"
)
async def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的统计数据

    返回：
    - total_interviews: 面试总次数
    - completed_interviews: 完成的面试次数
    - average_score: 平均评分
    - last_interview_time: 最近一次面试时间
    - member_since: 注册时间
    """
    interview_count = db.query(Interview).filter(Interview.user_id == current_user.id).count()

    completed_count = db.query(Interview).filter(
        Interview.user_id == current_user.id,
        Interview.status == "completed"
    ).count()

    assessments = db.query(Assessment).filter(Assessment.user_id == current_user.id).all()
    avg_score = sum(a.overall_score for a in assessments) / len(assessments) if assessments else 0

    last_interview = db.query(Interview).filter(
        Interview.user_id == current_user.id
    ).order_by(Interview.created_at.desc()).first()

    return {
        "total_interviews": interview_count,
        "completed_interviews": completed_count,
        "average_score": round(avg_score, 2),
        "last_interview_time": last_interview.created_at if last_interview else None,
        "member_since": current_user.created_at
    }
