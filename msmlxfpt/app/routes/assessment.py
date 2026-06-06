from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Assessment, Interview, InterviewQuestion, Question
from app.schemas import AssessmentResponse
from app.routes.auth import get_current_user
from app.models import User
from app.utils import calculate_score, generate_suggestions

router = APIRouter()

@router.post(
    "/{interview_id}",
    response_model=AssessmentResponse,
    tags=["评估"],
    summary="生成面试评估报告"
)
async def generate_assessment(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    为完成的面试生成AI评估报告

    - **interview_id**: 面试ID

    评估维度包括：
    - 综合得分（10分制）
    - 内容相关性：回答与岗位要求的匹配程度
    - 表达流利度：语言的流畅程度
    - 自信程度：回答的语气和态度
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")

    if interview.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限访问")

    interview_questions = db.query(InterviewQuestion).filter(
        InterviewQuestion.interview_id == interview_id
    ).order_by(InterviewQuestion.order_num).all()

    scores = []
    suggestions = []

    for iq in interview_questions:
        question = db.query(Question).filter(Question.id == iq.question_id).first()
        if iq.user_answer:
            score = calculate_score(iq.user_answer, question.keywords)
            scores.append(score)
            suggestion = generate_suggestions(score, question.content)
            suggestions.append(f"问题{iq.order_num}: {suggestion}")

    if scores:
        overall_score = sum(s["overall_score"] for s in scores) / len(scores)
        content_score = sum(s["content_score"] for s in scores) / len(scores)
        fluency_score = sum(s["fluency_score"] for s in scores) / len(scores)
        confidence_score = sum(s["confidence_score"] for s in scores) / len(scores)
    else:
        overall_score = 0
        content_score = 0
        fluency_score = 0
        confidence_score = 0

    report = generate_comprehensive_report(interview, scores, suggestions)

    assessment = Assessment(
        interview_id=interview_id,
        user_id=current_user.id,
        overall_score=round(overall_score, 2),
        content_score=round(content_score, 2),
        fluency_score=round(fluency_score, 2),
        confidence_score=round(confidence_score, 2),
        suggestions="\n\n".join(suggestions),
        report=report
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment

@router.get(
    "/{interview_id}",
    response_model=AssessmentResponse,
    tags=["评估"],
    summary="获取面试评估报告"
)
async def get_assessment(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取指定面试的评估报告

    - **interview_id**: 面试ID
    """
    assessment = db.query(Assessment).filter(Assessment.interview_id == interview_id).first()
    
    # 如果评估报告不存在，自动生成
    if not assessment:
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise HTTPException(status_code=404, detail="面试不存在")
        
        if interview.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="无权限访问")
        
        # 自动生成评估报告
        interview_questions = db.query(InterviewQuestion).filter(
            InterviewQuestion.interview_id == interview_id
        ).order_by(InterviewQuestion.order_num).all()

        scores = []
        suggestions = []
        questions_data = []

        for iq in interview_questions:
            question = db.query(Question).filter(Question.id == iq.question_id).first()
            
            # 收集题目数据（包含用户答案和参考答案）
            questions_data.append({
                "content": question.content,
                "user_answer": iq.user_answer,
                "answer": question.answer,
                "keywords": question.keywords
            })
            
            if iq.user_answer:
                score = calculate_score(iq.user_answer, question.keywords)
                scores.append(score)
                suggestion = generate_suggestions(score, question.content)
                suggestions.append(f"问题{iq.order_num}: {suggestion}")

        if scores:
            overall_score = sum(s["overall_score"] for s in scores) / len(scores)
            content_score = sum(s["content_score"] for s in scores) / len(scores)
            fluency_score = sum(s["fluency_score"] for s in scores) / len(scores)
            confidence_score = sum(s["confidence_score"] for s in scores) / len(scores)
        else:
            overall_score = 0
            content_score = 0
            fluency_score = 0
            confidence_score = 0

        report = generate_comprehensive_report(interview, scores, suggestions, questions_data)

        assessment = Assessment(
            interview_id=interview_id,
            user_id=current_user.id,
            overall_score=round(overall_score, 2),
            content_score=round(content_score, 2),
            fluency_score=round(fluency_score, 2),
            confidence_score=round(confidence_score, 2),
            suggestions="\n\n".join(suggestions),
            report=report
        )

        db.add(assessment)
        db.commit()
        db.refresh(assessment)

    if assessment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限访问")

    return assessment

@router.get(
    "/history/list",
    response_model=list[AssessmentResponse],
    tags=["评估"],
    summary="获取评估历史"
)
async def get_assessment_history(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的评估报告历史

    - **page**: 页码
    - **size**: 每页数量
    """
    assessments = db.query(Assessment).filter(
        Assessment.user_id == current_user.id
    ).order_by(Assessment.created_at.desc()).offset((page - 1) * size).limit(size).all()

    return assessments

def generate_comprehensive_report(interview, scores, suggestions, questions_data=None):
    """生成综合评估报告"""
    job_type_map = {
        "tech": "技术岗",
        "product": "产品岗",
        "operation": "运营岗",
        "design": "设计岗",
        "other": "其他"
    }

    difficulty_map = {
        "junior": "初级",
        "middle": "中级",
        "senior": "高级"
    }

    # 生成答案对比部分
    answers_section = ""
    if questions_data:
        answers_section = "\n## 答案对比\n\n"
        for idx, q_data in enumerate(questions_data, 1):
            answers_section += f"### 第{idx}题\n"
            answers_section += f"**问题**: {q_data.get('content', '')}\n\n"
            answers_section += f"**您的答案**: {q_data.get('user_answer', '未作答')}\n\n"
            answers_section += f"**参考答案**: {q_data.get('answer', '暂无参考答案')}\n\n"
            answers_section += f"**关键词**: {q_data.get('keywords', '')}\n\n"

    report = f"""# 面试评估报告

## 面试信息
- 岗位类型: {job_type_map.get(interview.job_type.value, interview.job_type.value)}
- 难度等级: {difficulty_map.get(interview.difficulty.value, interview.difficulty.value)}
- 面试时间: {interview.created_at.strftime('%Y-%m-%d %H:%M:%S')}

## 综合评分
| 维度 | 分数 | 评价 |
|------|------|------|
| 综合得分 | {round(sum(s['overall_score'] for s in scores) / len(scores), 1) if scores else 0}/10 | {get_score_level(sum(s['overall_score'] for s in scores) / len(scores) if scores else 0)} |
| 内容相关性 | {round(sum(s['content_score'] for s in scores) / len(scores), 1) if scores else 0}/10 | {get_score_level(sum(s['content_score'] for s in scores) / len(scores) if scores else 0)} |
| 表达流利度 | {round(sum(s['fluency_score'] for s in scores) / len(scores), 1) if scores else 0}/10 | {get_score_level(sum(s['fluency_score'] for s in scores) / len(scores) if scores else 0)} |
| 自信程度 | {round(sum(s['confidence_score'] for s in scores) / len(scores), 1) if scores else 0}/10 | {get_score_level(sum(s['confidence_score'] for s in scores) / len(scores) if scores else 0)} |

{answers_section}
## 改进建议
{chr(10).join(suggestions)}

## 总结
{get_summary(sum(s['overall_score'] for s in scores) / len(scores) if scores else 0)}
"""
    return report

def get_score_level(score):
    """获取评分等级"""
    if score >= 9:
        return "优秀"
    elif score >= 8:
        return "良好"
    elif score >= 6:
        return "中等"
    elif score >= 4:
        return "需改进"
    else:
        return "较差"

def get_summary(score):
    """获取总结"""
    if score >= 8:
        return "您的面试表现优秀！继续保持，可以尝试挑战更高难度的面试。"
    elif score >= 6:
        return "您的面试表现良好，但仍有提升空间。建议针对上述建议进行针对性练习。"
    else:
        return "建议多进行面试练习，加强基础知识学习，提升表达能力。"
