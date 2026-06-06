"""面试模块测试"""
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

def test_start_interview(setup_database):
    """测试开始面试"""
    # 先登录获取token
    login_response = client.post(
        "/api/auth/login",
        data={"username": "13800138001", "password": "user123"}
    )
    token = login_response.json()["access_token"]
    
    # 开始面试
    response = client.post(
        "/api/interview/start",
        json={"job_type": "tech", "difficulty": "junior"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["job_type"] == "tech"
    assert data["difficulty"] == "junior"
    assert data["status"] == "in_progress"

def test_get_interview_questions(setup_database):
    """测试获取面试题目"""
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
    response = client.get(
        f"/api/interview/{interview_id}/questions",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    questions = response.json()
    assert len(questions) > 0
    assert "content" in questions[0]

def test_submit_answer(setup_database):
    """测试提交答案"""
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
    question_id = questions_response.json()[0]["id"]
    
    # 提交答案
    response = client.post(
        f"/api/interview/{interview_id}/answer",
        params={"question_id": question_id, "answer": "这是我的回答", "answer_time": 30},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "答案提交成功" in response.json()["message"]

def test_complete_interview(setup_database):
    """测试完成面试"""
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
    
    # 完成面试
    response = client.post(
        f"/api/interview/{interview_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["completed_at"] is not None

def test_get_interview_history(setup_database):
    """测试获取面试历史"""
    # 先登录获取token
    login_response = client.post(
        "/api/auth/login",
        data={"username": "13800138001", "password": "user123"}
    )
    token = login_response.json()["access_token"]
    
    # 获取面试历史
    response = client.get(
        "/api/interview/history",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
