"""用户认证模块测试"""
import pytest
from fastapi.testclient import TestClient
from main import app

# 创建测试客户端
client = TestClient(app)

def test_register():
    """测试用户注册"""
    response = client.post(
        "/api/auth/register",
        json={
            "phone": "13800138002",
            "email": "test@example.com",
            "password": "password123",
            "nickname": "测试用户"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "13800138002"
    assert data["email"] == "test@example.com"
    assert data["nickname"] == "测试用户"
    assert data["role"] == "user"

def test_register_duplicate_phone():
    """测试重复手机号注册"""
    response = client.post(
        "/api/auth/register",
        json={
            "phone": "13800138002",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "手机号已被注册" in response.json()["detail"]

def test_login():
    """测试用户登录"""
    response = client.post(
        "/api/auth/login",
        data={"username": "13800138002", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "user"

def test_login_wrong_password():
    """测试错误密码登录"""
    response = client.post(
        "/api/auth/login",
        data={"username": "13800138002", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "用户名或密码错误" in response.json()["detail"]

def test_forget_password():
    """测试忘记密码"""
    response = client.post(
        "/api/auth/forget-password",
        params={"phone": "13800138002"}
    )
    assert response.status_code == 200
    assert "验证码已发送" in response.json()["message"]

def test_forget_password_not_found():
    """测试忘记密码-用户不存在"""
    response = client.post(
        "/api/auth/forget-password",
        params={"phone": "13800138099"}
    )
    assert response.status_code == 400
    assert "该手机号未注册" in response.json()["detail"]

def test_reset_password():
    """测试重置密码"""
    response = client.post(
        "/api/auth/reset-password",
        params={
            "phone": "13800138002",
            "code": "123456",
            "new_password": "newpassword123"
        }
    )
    assert response.status_code == 200
    assert "密码重置成功" in response.json()["message"]

def test_reset_password_wrong_code():
    """测试重置密码-验证码错误"""
    response = client.post(
        "/api/auth/reset-password",
        params={
            "phone": "13800138002",
            "code": "654321",
            "new_password": "newpassword123"
        }
    )
    assert response.status_code == 400
    assert "验证码错误" in response.json()["detail"]
