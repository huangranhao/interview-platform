from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import LearningResource, LearningRecord, JobType, InterviewDifficulty
from app.schemas import LearningResourceResponse, LearningResourceCreate, LearningRecordResponse, LearningRecordCreate
from app.routes.auth import get_current_user
from app.models import User

router = APIRouter()

def serialize_resource(resource):
    """序列化学习资源对象，将枚举转换为字符串"""
    return {
        "id": resource.id,
        "title": resource.title,
        "content": resource.content,
        "resource_type": resource.resource_type,
        "job_type": resource.job_type.value if hasattr(resource.job_type, 'value') else resource.job_type,
        "difficulty": resource.difficulty.value if hasattr(resource.difficulty, 'value') else resource.difficulty,
        "view_count": resource.view_count,
        "created_at": resource.created_at,
        "updated_at": resource.updated_at
    }

@router.get(
    "/resources",
    tags=["学习中心"],
    summary="获取学习资源列表"
)
async def get_learning_resources(
    job_type: Optional[str] = Query(None, description="岗位类型"),
    difficulty: Optional[str] = Query(None, description="难度等级"),
    resource_type: Optional[str] = Query(None, description="资源类型：article/video"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取面试技巧学习资源列表

    - **job_type**: 按岗位类型筛选（可选）
    - **difficulty**: 按难度筛选（可选）
    - **resource_type**: 资源类型 article(文章)/video(视频)
    - **page**: 页码
    - **size**: 每页数量
    """
    query = db.query(LearningResource)

    if job_type:
        query = query.filter(LearningResource.job_type == JobType(job_type))

    if difficulty:
        query = query.filter(LearningResource.difficulty == InterviewDifficulty(difficulty))

    if resource_type:
        query = query.filter(LearningResource.resource_type == resource_type)

    resources = query.order_by(LearningResource.created_at.desc()).offset((page - 1) * size).limit(size).all()

    return [serialize_resource(r) for r in resources]

@router.get(
    "/resources/{resource_id}",
    tags=["学习中心"],
    summary="获取学习资源详情"
)
async def get_learning_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    """
    获取学习资源详细信息，同时增加浏览次数

    - **resource_id**: 资源ID
    """
    resource = db.query(LearningResource).filter(LearningResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="资源不存在")

    resource.view_count += 1
    db.commit()

    return serialize_resource(resource)

@router.post(
    "/resources",
    tags=["学习中心"],
    summary="创建学习资源"
)
async def create_learning_resource(
    resource: LearningResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新的学习资源（仅管理员可用）

    - **title**: 资源标题
    - **content**: 资源内容
    - **resource_type**: 资源类型
    - **job_type**: 岗位类型
    - **difficulty**: 难度等级
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权限创建资源")

    new_resource = LearningResource(
        title=resource.title,
        content=resource.content,
        resource_type=resource.resource_type,
        job_type=JobType(resource.job_type),
        difficulty=InterviewDifficulty(resource.difficulty)
    )

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return serialize_resource(new_resource)

@router.put(
    "/resources/{resource_id}",
    tags=["学习中心"],
    summary="更新学习资源"
)
async def update_learning_resource(
    resource_id: int,
    resource: LearningResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新学习资源（仅管理员可用）

    - **resource_id**: 资源ID
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权限更新资源")

    db_resource = db.query(LearningResource).filter(LearningResource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="资源不存在")

    db_resource.title = resource.title
    db_resource.content = resource.content
    db_resource.resource_type = resource.resource_type
    db_resource.job_type = JobType(resource.job_type)
    db_resource.difficulty = InterviewDifficulty(resource.difficulty)

    db.commit()
    db.refresh(db_resource)

    return serialize_resource(db_resource)

@router.delete(
    "/resources/{resource_id}",
    tags=["学习中心"],
    summary="删除学习资源"
)
async def delete_learning_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除学习资源（仅管理员可用）

    - **resource_id**: 资源ID
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权限删除资源")

    resource = db.query(LearningResource).filter(LearningResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="资源不存在")

    db.delete(resource)
    db.commit()

    return {"message": "资源删除成功"}

@router.post(
    "/records",
    response_model=LearningRecordResponse,
    tags=["学习中心"],
    summary="创建或更新学习记录"
)
async def create_learning_record(
    record: LearningRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    记录用户学习进度

    - **resource_id**: 资源ID
    - **progress**: 学习进度（0-100）
    - **completed**: 是否已完成
    """
    resource = db.query(LearningResource).filter(LearningResource.id == record.resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="资源不存在")

    existing_record = db.query(LearningRecord).filter(
        LearningRecord.user_id == current_user.id,
        LearningRecord.resource_id == record.resource_id
    ).first()

    if existing_record:
        existing_record.progress = record.progress
        existing_record.completed = record.completed
        db.commit()
        db.refresh(existing_record)
        return existing_record

    new_record = LearningRecord(
        user_id=current_user.id,
        resource_id=record.resource_id,
        progress=record.progress,
        completed=record.completed
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record

@router.get(
    "/records",
    response_model=List[LearningRecordResponse],
    tags=["学习中心"],
    summary="获取学习记录"
)
async def get_learning_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的所有学习记录
    """
    records = db.query(LearningRecord).filter(
        LearningRecord.user_id == current_user.id
    ).order_by(LearningRecord.updated_at.desc()).all()

    return records

@router.get(
    "/progress",
    tags=["学习中心"],
    summary="获取学习进度统计"
)
async def get_learning_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的学习进度统计信息

    返回：
    - total_resources: 学习资源总数
    - completed_resources: 已完成资源数
    - average_progress: 平均进度
    - completion_rate: 完成率百分比
    """
    total_records = db.query(LearningRecord).filter(
        LearningRecord.user_id == current_user.id
    ).count()

    completed_records = db.query(LearningRecord).filter(
        LearningRecord.user_id == current_user.id,
        LearningRecord.completed == True
    ).count()

    avg_progress = db.query(LearningRecord.progress).filter(
        LearningRecord.user_id == current_user.id
    ).all()

    avg_progress_value = sum(p[0] for p in avg_progress) / len(avg_progress) if avg_progress else 0

    return {
        "total_resources": total_records,
        "completed_resources": completed_records,
        "average_progress": round(avg_progress_value, 2),
        "completion_rate": round((completed_records / total_records) * 100, 2) if total_records > 0 else 0
    }
