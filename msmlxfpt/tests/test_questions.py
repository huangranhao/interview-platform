"""题库模块测试"""
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

def test_get_questions(setup_database):
    """测试获取题库列表"""
    response = client.get("/api/questions/")
    assert response.status_code == 200
    questions = response.json()
    assert isinstance(questions, list)

def test_get_questions_filtered(setup_database):
    """测试按条件筛选题目"""
    response = client.get("/api/questions/?job_type=tech&difficulty=junior")
    assert response.status_code == 200
    questions = response.json()
    for q in questions:
        assert q["job_type"] == "tech"
        assert q["difficulty"] == "junior"

def test_search_questions(setup_database):
    """测试搜索题目"""
    response = client.get("/api/questions/?keyword=装饰器")
    assert response.status_code == 200
    questions = response.json()
    assert isinstance(questions, list)

def test_get_question_detail(setup_database):
    """测试获取题目详情"""
    # 先获取题目列表
    list_response = client.get("/api/questions/")
    questions = list_response.json()
    
    if questions:
        question_id = questions[0]["id"]
        response = client.get(f"/api/questions/{question_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == question_id
        assert "content" in data

def test_favorite_question(setup_database):
    """测试收藏题目"""
    # 先登录获取token
    login_response = client.post(
        "/api/auth/login",
        data={"username": "13800138001", "password": "user123"}
    )
    token = login_response.json()["access_token"]
    
    # 获取题目列表
    list_response = client.get("/api/questions/")
    questions = list_response.json()
    
    if questions:
        question_id = questions[0]["id"]
        response = client.post(
            f"/api/questions/{question_id}/favorite",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert "收藏成功" in response.json()["message"]

def test_unfavorite_question(setup_database):
    """测试取消收藏"""
    # 先登录获取token
    login_response = client.post(
        "/api/auth/login",
        data={"username": "13800138001", "password": "user123"}
    )
    token = login_response.json()["access_token"]
    
    # 获取题目列表
    list_response = client.get("/api/questions/")
    questions = list_response.json()
    
    if questions:
        question_id = questions[0]["id"]
        response = client.delete(
            f"/api/questions/{question_id}/favorite",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert "取消收藏成功" in response.json()["message"]

def test_get_favorites(setup_database):
    """测试获取收藏列表"""
    # 先登录获取token
    login_response = client.post(
        "/api/auth/login",
        data={"username": "13800138001", "password": "user123"}
    )
    token = login_response.json()["access_token"]
    
    response = client.get(
        "/api/questions/favorites",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
