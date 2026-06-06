from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Enterprise, CustomQuestion, EnterpriseCandidate, Interview, User, InterviewDifficulty
from app.schemas import EnterpriseCreate, EnterpriseResponse, CustomQuestionCreate, CustomQuestionResponse, EnterpriseCandidateResponse
from app.routes.auth import get_current_user
from app.models import User as UserModel

router = APIRouter()

@router.post(
    "/register",
    response_model=EnterpriseResponse,
    tags=["企业端"],
    summary="企业注册认证"
)
async def register_enterprise(
    enterprise: EnterpriseCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    企业用户注册认证

    - **name**: 企业名称
    - **industry**: 所属行业
    - **scale**: 企业规模
    - **description**: 企业简介
    """
    existing = db.query(Enterprise).filter(Enterprise.user_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="您已注册过企业账号")

    new_enterprise = Enterprise(
        user_id=current_user.id,
        name=enterprise.name,
        industry=enterprise.industry,
        scale=enterprise.scale,
        description=enterprise.description,
        is_verified=False
    )

    db.add(new_enterprise)
    db.commit()
    db.refresh(new_enterprise)

    return new_enterprise

@router.get(
    "/profile",
    response_model=EnterpriseResponse,
    tags=["企业端"],
    summary="获取企业信息"
)
async def get_enterprise_profile(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    获取当前企业的认证信息
    """
    enterprise = db.query(Enterprise).filter(Enterprise.user_id == current_user.id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="企业信息不存在")

    return enterprise

@router.put(
    "/profile",
    response_model=EnterpriseResponse,
    tags=["企业端"],
    summary="更新企业信息"
)
async def update_enterprise_profile(
    enterprise: EnterpriseCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    更新企业基本信息
    """
    db_enterprise = db.query(Enterprise).filter(Enterprise.user_id == current_user.id).first()
    if not db_enterprise:
        raise HTTPException(status_code=404, detail="企业信息不存在")

    db_enterprise.name = enterprise.name
    db_enterprise.industry = enterprise.industry
    db_enterprise.scale = enterprise.scale
    db_enterprise.description = enterprise.description

    db.commit()
    db.refresh(db_enterprise)

    return db_enterprise

@router.post(
    "/questions",
    response_model=CustomQuestionResponse,
    tags=["企业端"],
    summary="创建自定义题目"
)
async def create_custom_question(
    question: CustomQuestionCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    企业创建自定义面试题目

    - **content**: 题目内容
    - **answer**: 参考答案
    - **difficulty**: 难度等级
    """
    enterprise = db.query(Enterprise).filter(Enterprise.user_id == current_user.id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="企业信息不存在")

    new_question = CustomQuestion(
        enterprise_id=enterprise.id,
        content=question.content,
        answer=question.answer,
        difficulty=InterviewDifficulty(question.difficulty)
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question

@router.get(
    "/questions",
    response_model=List[CustomQuestionResponse],
    tags=["企业端"],
    summary="获取企业题库"
)
async def get_custom_questions(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    获取当前企业的所有自定义题目
    """
    enterprise = db.query(Enterprise).filter(Enterprise.user_id == current_user.id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="企业信息不存在")

    questions = db.query(CustomQuestion).filter(
        CustomQuestion.enterprise_id == enterprise.id
    ).all()

    return questions

@router.delete(
    "/questions/{question_id}",
    tags=["企业端"],
    summary="删除自定义题目"
)
async def delete_custom_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    删除企业的自定义题目

    - **question_id**: 题目ID
    """
    enterprise = db.query(Enterprise).filter(Enterprise.user_id == current_user.id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="企业信息不存在")

    question = db.query(CustomQuestion).filter(
        CustomQuestion.id == question_id,
        CustomQuestion.enterprise_id == enterprise.id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")

    db.delete(question)
    db.commit()

    return {"message": "题目删除成功"}

@router.post(
    "/candidates/{user_id}",
    response_model=EnterpriseCandidateResponse,
    tags=["企业端"],
    summary="添加候选人"
)
async def add_candidate(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    将求职者添加到企业候选人列表

    - **user_id**: 求职者用户ID
    """
    enterprise = db.query(Enterprise).filter(Enterprise.user_id == current_user.id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="企业信息不存在")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    existing = db.query(EnterpriseCandidate).filter(
        EnterpriseCandidate.enterprise_id == enterprise.id,
        EnterpriseCandidate.user_id == user_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="该候选人已添加")

    candidate = EnterpriseCandidate(
        enterprise_id=enterprise.id,
        user_id=user_id,
        status="pending"
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate

@router.get(
    "/candidates",
    response_model=List[EnterpriseCandidateResponse],
    tags=["企业端"],
    summary="获取候选人列表"
)
async def get_candidates(
    status: Optional[str] = Query(None, description="筛选状态：pending/reviewed/offered/rejected"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    获取企业的候选人列表

    - **status**: 按状态筛选（可选）
    """
    enterprise = db.query(Enterprise).filter(Enterprise.user_id == current_user.id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="企业信息不存在")

    query = db.query(EnterpriseCandidate).filter(EnterpriseCandidate.enterprise_id == enterprise.id)

    if status:
        query = query.filter(EnterpriseCandidate.status == status)

    candidates = query.all()

    return candidates

@router.put(
    "/candidates/{candidate_id}",
    response_model=EnterpriseCandidateResponse,
    tags=["企业端"],
    summary="更新候选人状态"
)
async def update_candidate_status(
    candidate_id: int,
    status: str = Query(..., description="新状态"),
    score: Optional[float] = Query(None, description="评分"),
    notes: Optional[str] = Query(None, description="备注"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    更新候选人的面试状态和评分

    - **candidate_id**: 候选人ID
    - **status**: 新状态 pending/reviewed/offered/rejected
    - **score**: 面试评分（可选）
    - **notes**: 备注信息（可选）
    """
    enterprise = db.query(Enterprise).filter(Enterprise.user_id == current_user.id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="企业信息不存在")

    candidate = db.query(EnterpriseCandidate).filter(
        EnterpriseCandidate.id == candidate_id,
        EnterpriseCandidate.enterprise_id == enterprise.id
    ).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")

    candidate.status = status
    if score is not None:
        candidate.score = score
    if notes is not None:
        candidate.notes = notes

    db.commit()
    db.refresh(candidate)

    return candidate

@router.get(
    "/candidates/{candidate_id}/interviews",
    tags=["企业端"],
    summary="查看候选人面试记录"
)
async def get_candidate_interviews(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    查看候选人的所有面试记录

    - **candidate_id**: 候选人ID
    """
    enterprise = db.query(Enterprise).filter(Enterprise.user_id == current_user.id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="企业信息不存在")

    candidate = db.query(EnterpriseCandidate).filter(
        EnterpriseCandidate.id == candidate_id,
        EnterpriseCandidate.enterprise_id == enterprise.id
    ).first()

    if not candidate:
        raise HTTPException(status_code=403, detail="无权限访问")

    interviews = db.query(Interview).filter(Interview.user_id == candidate.user_id).all()

    result = []
    for interview in interviews:
        result.append({
            "id": interview.id,
            "job_type": interview.job_type.value,
            "difficulty": interview.difficulty.value,
            "status": interview.status,
            "video_url": interview.video_url,
            "created_at": interview.created_at,
            "completed_at": interview.completed_at
        })

    return result
