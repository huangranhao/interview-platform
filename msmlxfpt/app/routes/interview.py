from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Interview, Question, InterviewQuestion, JobType, InterviewDifficulty
from app.schemas import InterviewCreate, InterviewResponse, InterviewQuestionResponse
from app.routes.auth import get_current_user
from app.models import User
import random

router = APIRouter()

def serialize_interview(interview):
    """序列化面试对象，将枚举转换为字符串"""
    return {
        "id": interview.id,
        "user_id": interview.user_id,
        "job_type": interview.job_type.value if hasattr(interview.job_type, 'value') else interview.job_type,
        "difficulty": interview.difficulty.value if hasattr(interview.difficulty, 'value') else interview.difficulty,
        "status": interview.status,
        "duration": interview.duration,
        "video_url": interview.video_url,
        "created_at": interview.created_at,
        "completed_at": interview.completed_at
    }

@router.post(
    "/start",
    tags=["面试"],
    summary="开始模拟面试"
)
async def start_interview(
    interview_create: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    开始一场新的模拟面试

    - **job_type**: 岗位类型，可选值：tech(技术)、product(产品)、operation(运营)、design(设计)、other(其他)
    - **difficulty**: 难度等级，可选值：junior(初级)、middle(中级)、senior(高级)
    - **duration**: 面试时长（秒），默认300秒（5分钟）

    系统会根据选择的岗位和难度，随机从题库中抽取5道题目
    """
    interview = Interview(
        user_id=current_user.id,
        job_type=JobType(interview_create.job_type),
        difficulty=InterviewDifficulty(interview_create.difficulty),
        status="in_progress",
        duration=interview_create.duration
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    questions = db.query(Question).filter(
        Question.job_type == interview.job_type,
        Question.difficulty == interview.difficulty
    ).all()

    if len(questions) < 5:
        additional_questions = db.query(Question).filter(
            Question.job_type == interview.job_type
        ).all()
        questions = list(set(questions + additional_questions))

    selected_questions = random.sample(questions, min(5, len(questions)))

    for idx, question in enumerate(selected_questions, 1):
        interview_question = InterviewQuestion(
            interview_id=interview.id,
            question_id=question.id,
            order_num=idx
        )
        db.add(interview_question)

    db.commit()

    return serialize_interview(interview)

@router.get(
    "/{interview_id}/questions",
    tags=["面试"],
    summary="获取面试题目列表"
)
async def get_interview_questions(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取指定面试的题目列表

    - **interview_id**: 面试ID

    返回该面试的所有题目，包括题目内容、用户回答、回答时长等信息
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")

    if interview.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限访问")

    questions = db.query(InterviewQuestion).filter(
        InterviewQuestion.interview_id == interview_id
    ).order_by(InterviewQuestion.order_num).all()

    result = []
    for iq in questions:
        question = db.query(Question).filter(Question.id == iq.question_id).first()
        result.append({
            "id": iq.id,
            "question_id": iq.question_id,
            "content": question.content,
            "keywords": question.keywords,
            "order_num": iq.order_num,
            "user_answer": iq.user_answer,
            "answer_time": iq.answer_time
        })

    return result

@router.post(
    "/{interview_id}/answer",
    tags=["面试"],
    summary="提交面试答案"
)
async def submit_answer(
    interview_id: int,
    answer_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    提交用户对某个问题的回答

    - **interview_id**: 面试ID
    - **question_id**: 题目ID（InterviewQuestion的id）
    - **answer**: 用户回答内容
    - **answer_time**: 回答时长（秒）
    """
    question_id = answer_data.get('question_id')
    answer = answer_data.get('answer')
    answer_time = answer_data.get('answer_time')
    
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")

    if interview.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限访问")

    interview_question = db.query(InterviewQuestion).filter(
        InterviewQuestion.interview_id == interview_id,
        InterviewQuestion.id == question_id
    ).first()

    if not interview_question:
        raise HTTPException(status_code=404, detail="面试题目不存在")

    interview_question.user_answer = answer
    interview_question.answer_time = answer_time

    db.commit()

    return {"message": "答案提交成功"}

@router.post(
    "/{interview_id}/complete",
    tags=["面试"],
    summary="完成面试"
)
async def complete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    标记面试为已完成状态

    - **interview_id**: 面试ID

    完成面试后才能生成评估报告
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")

    if interview.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限访问")

    interview.status = "completed"
    interview.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(interview)

    return serialize_interview(interview)

@router.get(
    "/history",
    tags=["面试"],
    summary="获取面试历史记录"
)
async def get_interview_history(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的面试历史记录

    - **page**: 页码，从1开始
    - **size**: 每页记录数，最大100

    按时间倒序返回面试记录
    """
    interviews = db.query(Interview).filter(
        Interview.user_id == current_user.id
    ).order_by(Interview.created_at.desc()).offset((page - 1) * size).limit(size).all()

    return [serialize_interview(i) for i in interviews]

@router.get(
    "/{interview_id}",
    tags=["面试"],
    summary="获取面试详情"
)
async def get_interview_detail(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取指定面试的详细信息

    - **interview_id**: 面试ID
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")

    if interview.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限访问")

    return serialize_interview(interview)

@router.delete(
    "/{interview_id}",
    tags=["面试"],
    summary="删除面试记录"
)
async def delete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除指定的面试记录

    - **interview_id**: 面试ID

    只能删除自己的面试记录
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")

    if interview.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除")

    # 删除相关的面试题目记录
    db.query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview_id).delete()
    
    # 删除面试记录
    db.delete(interview)
    db.commit()

    return {"message": "面试记录已删除", "interview_id": interview_id}
