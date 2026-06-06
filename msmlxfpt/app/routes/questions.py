from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Question, FavoriteQuestion, JobType, InterviewDifficulty
from app.schemas import QuestionResponse, QuestionCreate, QuestionSearch
from app.routes.auth import get_current_user
from app.models import User

router = APIRouter()

def serialize_question(question):
    """序列化题目对象，将枚举转换为字符串"""
    return {
        "id": question.id,
        "job_type": question.job_type.value if hasattr(question.job_type, 'value') else question.job_type,
        "difficulty": question.difficulty.value if hasattr(question.difficulty, 'value') else question.difficulty,
        "content": question.content,
        "answer": question.answer,
        "keywords": question.keywords,
        "created_at": question.created_at
    }

@router.get(
    "/",
    tags=["题库"],
    summary="获取面试题库列表"
)
async def get_questions(
    job_type: Optional[str] = Query(None, description="岗位类型：tech/product/operation/design/other"),
    difficulty: Optional[str] = Query(None, description="难度等级：junior/middle/senior"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取面试题库列表，支持多种筛选条件

    - **job_type**: 岗位类型筛选（可选）
    - **difficulty**: 难度等级筛选（可选）
    - **keyword**: 关键词搜索，匹配题目内容或关键字（可选）
    - **page**: 页码，默认第1页
    - **size**: 每页数量，默认10条，最大100条
    """
    query = db.query(Question)

    if job_type:
        query = query.filter(Question.job_type == JobType(job_type))

    if difficulty:
        query = query.filter(Question.difficulty == InterviewDifficulty(difficulty))

    if keyword:
        query = query.filter(Question.content.contains(keyword) | Question.keywords.contains(keyword))

    questions = query.offset((page - 1) * size).limit(size).all()

    return [serialize_question(q) for q in questions]

@router.get(
    "/{question_id}",
    tags=["题库"],
    summary="获取题目详情"
)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    """
    获取单个题目的详细信息

    - **question_id**: 题目ID
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    return serialize_question(question)

@router.post(
    "/",
    tags=["题库"],
    summary="创建新题目"
)
async def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新的面试题目（仅管理员可用）

    - **job_type**: 岗位类型
    - **difficulty**: 难度等级
    - **content**: 题目内容
    - **answer**: 参考答案
    - **keywords**: 关键字（用逗号分隔）
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权限创建题目")

    new_question = Question(
        job_type=JobType(question.job_type),
        difficulty=InterviewDifficulty(question.difficulty),
        content=question.content,
        answer=question.answer,
        keywords=question.keywords
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return serialize_question(new_question)

@router.put(
    "/{question_id}",
    tags=["题库"],
    summary="更新题目"
)
async def update_question(
    question_id: int,
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新面试题目（仅管理员可用）

    - **question_id**: 题目ID
    - 其他参数同创建题目
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权限更新题目")

    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="题目不存在")

    db_question.job_type = JobType(question.job_type)
    db_question.difficulty = InterviewDifficulty(question.difficulty)
    db_question.content = question.content
    db_question.answer = question.answer
    db_question.keywords = question.keywords

    db.commit()
    db.refresh(db_question)

    return serialize_question(db_question)

@router.delete(
    "/{question_id}",
    tags=["题库"],
    summary="删除题目"
)
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除面试题目（仅管理员可用）

    - **question_id**: 题目ID
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权限删除题目")

    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")

    db.delete(question)
    db.commit()

    return {"message": "题目删除成功"}

@router.post(
    "/{question_id}/favorite",
    tags=["题库"],
    summary="收藏题目"
)
async def favorite_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    收藏指定的面试题目

    - **question_id**: 题目ID
    """
    existing = db.query(FavoriteQuestion).filter(
        FavoriteQuestion.user_id == current_user.id,
        FavoriteQuestion.question_id == question_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="已收藏该题目")

    favorite = FavoriteQuestion(
        user_id=current_user.id,
        question_id=question_id
    )

    db.add(favorite)
    db.commit()

    return {"message": "收藏成功"}

@router.delete(
    "/{question_id}/favorite",
    tags=["题库"],
    summary="取消收藏"
)
async def unfavorite_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    取消收藏指定的面试题目

    - **question_id**: 题目ID
    """
    favorite = db.query(FavoriteQuestion).filter(
        FavoriteQuestion.user_id == current_user.id,
        FavoriteQuestion.question_id == question_id
    ).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="未收藏该题目")

    db.delete(favorite)
    db.commit()

    return {"message": "取消收藏成功"}

@router.get(
    "/favorites/list",
    tags=["题库"],
    summary="获取收藏列表"
)
async def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户收藏的所有题目
    """
    favorites = db.query(FavoriteQuestion).filter(FavoriteQuestion.user_id == current_user.id).all()
    question_ids = [f.question_id for f in favorites]
    questions = db.query(Question).filter(Question.id.in_(question_ids)).all()
    return [serialize_question(q) for q in questions]
