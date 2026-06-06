"""评估模块测试"""
import pytest
from fastapi.testclient import TestClient
from app.database import Base, engine
from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    """设置测试数据库"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_generate_assessment(setup_database):
    """测试生成评估报告"""
    # 先登录获取token
    login_response = client.post(
        "/api/auth/login",
        data={"username": "13800138001", "password": "user123"}
    )
    token = login_response.json()["access_token"]
    
    # 开始面试
    interview_response = client.post(
        "/api/interview/start",
        json={"job_type": "tech", "difficulty": "junior"},
        headers={"Authorization": f"Bearer {token}"}
    )
    interview_id = interview_response.json()["id"]
    
    # 获取面试题目
    questions_response = client.get(
        f"/api/interview/{interview_id}/questions",
        headers={"Authorization": f"Bearer {token}"}
    )
    questions = questions_response.json()
    
    # 提交答案
    for question in questions:
        client.post(
            f"/api/interview/{interview_id}/answer",
            params={"question_id": question["id"], "answer": "这是我的详细回答内容，包含关键词信息", "answer_time": 45},
            headers={"Authorization": f"Bearer {token}"}
        )
    
    # 完成面试
    client.post(
        f"/api/interview/{interview_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 生成评估报告
    response = client.post(
        f"/api/assessment/{interview_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert "content_score" in data
    assert "fluency_score" in data
    assert "confidence_score" in data
    assert "suggestions" in data
    assert "report" in data
    
    # 验证评分范围
    assert 0 <= data["overall_score"] <= 10
    assert 0 <= data["content_score"] <= 10
    assert 0 <= data["fluency_score"] <= 10
    assert 0 <= data["confidence_score"] <= 10

def test_get_assessment(setup_database):
    """测试获取评估报告"""
    # 先登录获取token
    login_response = client.post(
        "/api/auth/login",
        data={"username": "13800138001", "password": "user123"}
    )
    token = login_response.json()["access_token"]
    
    # 开始面试
    interview_response = client.post(
        "/api/interview/start",
        json={"job_type": "tech", "difficulty": "junior"},
        headers={"Authorization": f"Bearer {token}"}
    )
    interview_id = interview_response.json()["id"]
    
    # 获取面试题目
    questions_response = client.get(
        f"/api/interview/{interview_id}/questions",
        headers={"Authorization": f"Bearer {token}"}
    )
    questions = questions_response.json()
    
    # 提交答案
    for question in questions:
        client.post(
            f"/api/interview/{interview_id}/answer",
            params={"question_id": question["id"], "answer": "这是回答", "answer_time": 30},
            headers={"Authorization": f"Bearer {token}"}
        )
    
    # 完成面试
    client.post(
        f"/api/interview/{interview_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 生成评估报告
    client.post(
        f"/api/assessment/{interview_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 获取评估报告
    response = client.get(
        f"/api/assessment/{interview_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert "report" in data

def test_get_assessment_history(setup_database):
    """测试获取评估报告历史"""
    # 先登录获取token
    login_response = client.post(
        "/api/auth/login",
        data={"username": "13800138001", "password": "user123"}
    )
    token = login_response.json()["access_token"]
    
    # 获取评估历史
    response = client.get(
        "/api/assessment/history",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
