from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

from app.database import get_db
from app.models import User, UserRole
from app.schemas import UserCreate, UserLogin, Token, UserResponse
from app.utils import verify_password, get_password_hash, create_access_token, generate_nickname

# 加载环境变量
load_dotenv()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    scheme_name="密码登录",
    description="请输入手机号/邮箱和密码进行登录"
)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def validate_password(password: str):
    """
    验证密码强度
    
    要求：
    - 长度至少8位
    - 包含至少一个数字
    - 包含至少一个小写字母
    - 包含至少一个大写字母
    - 包含至少一个特殊字符
    """
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="密码长度至少8位")
    
    if not any(char.isdigit() for char in password):
        raise HTTPException(status_code=400, detail="密码必须包含至少一个数字")
    
    if not any(char.islower() for char in password):
        raise HTTPException(status_code=400, detail="密码必须包含至少一个小写字母")
    
    if not any(char.isupper() for char in password):
        raise HTTPException(status_code=400, detail="密码必须包含至少一个大写字母")
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(char in special_chars for char in password):
        raise HTTPException(status_code=400, detail="密码必须包含至少一个特殊字符")

@router.post("/register", tags=["认证"], summary="用户注册")
async def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册接口
    
    - **phone**: 手机号（必填）
    - **email**: 邮箱（可选）
    - **password**: 密码（必填）- 要求：至少8位，包含数字、大小写字母和特殊字符
    - **nickname**: 昵称（可选，不填则自动生成）
    """
    # 验证密码强度
    validate_password(user_create.password)
    
    # 检查手机号是否已存在
    if db.query(User).filter(User.phone == user_create.phone).first():
        raise HTTPException(status_code=400, detail="手机号已被注册")
    
    # 检查邮箱是否已存在
    if user_create.email and db.query(User).filter(User.email == user_create.email).first():
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    # 创建用户
    password_hash = get_password_hash(user_create.password)
    user = User(
        phone=user_create.phone,
        email=user_create.email,
        password_hash=password_hash,
        nickname=user_create.nickname or generate_nickname(),
        role=UserRole(user_create.role) if user_create.role else UserRole.USER
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 手动序列化用户对象，将枚举转换为字符串
    return {
        "id": user.id,
        "phone": user.phone,
        "email": user.email,
        "nickname": user.nickname,
        "role": user.role.value,
        "is_active": user.is_active,
        "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }

@router.post("/login", response_model=Token, tags=["认证"], summary="用户登录")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    
    - **username**: 手机号或邮箱（在表单中作为 username 字段）
    - **password**: 密码
    
    返回访问令牌，用于后续接口认证
    """
    # 尝试通过手机号或邮箱登录
    user = db.query(User).filter(
        (User.phone == form_data.username) | (User.email == form_data.username)
    ).first()
    
    # 用户不存在
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="该用户未注册，请先注册再登录",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 密码错误
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="密码错误，请重新输入",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "user_id": user.id, 
        "role": user.role.value
    }

@router.post("/forget-password", tags=["认证"], summary="忘记密码")
async def forget_password(phone: str, db: Session = Depends(get_db)):
    """
    忘记密码接口
    
    - **phone**: 手机号
    
    系统会发送验证码到该手机号（演示环境验证码固定为 123456）
    """
    user = db.query(User).filter(User.phone == phone).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="该手机号未注册")
    
    # 模拟发送验证码（实际项目中需要调用短信 API）
    verification_code = "123456"  # 模拟验证码
    
    return {"message": "验证码已发送", "verification_code": verification_code}

@router.post("/reset-password", tags=["认证"], summary="重置密码")
async def reset_password(phone: str, code: str, new_password: str, db: Session = Depends(get_db)):
    """
    重置密码接口
    
    - **phone**: 手机号
    - **code**: 验证码（演示环境固定为 123456）
    - **new_password**: 新密码
    """
    # 验证验证码（模拟）
    if code != "123456":
        raise HTTPException(status_code=400, detail="验证码错误")
    
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在")
    
    # 更新密码
    user.password_hash = get_password_hash(new_password)
    db.commit()
    
    return {"message": "密码重置成功"}

@router.get("/me", tags=["认证"], summary="获取当前用户信息")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户的信息
    
    需要在请求头中携带 Authorization: Bearer {token}
    """
    return {
        "id": current_user.id,
        "phone": current_user.phone,
        "email": current_user.email,
        "nickname": current_user.nickname,
        "role": current_user.role.value,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }

@router.put("/me", tags=["认证"], summary="更新当前用户信息")
async def update_user_info(
    user_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新当前用户的信息
    
    - **nickname**: 昵称（可选）
    - **phone**: 手机号（可选）
    - **email**: 邮箱（可选）
    - **password**: 新密码（可选，留空表示不修改）
    
    需要在请求头中携带 Authorization: Bearer {token}
    """
    # 更新昵称
    if 'nickname' in user_data and user_data['nickname']:
        current_user.nickname = user_data['nickname']
    
    # 更新手机号
    if 'phone' in user_data and user_data['phone']:
        # 检查新手机号是否已被其他用户使用
        existing_user = db.query(User).filter(
            User.phone == user_data['phone'],
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="手机号已被注册")
        current_user.phone = user_data['phone']
    
    # 更新邮箱
    if 'email' in user_data and user_data['email']:
        # 检查新邮箱是否已被其他用户使用
        existing_user = db.query(User).filter(
            User.email == user_data['email'],
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="邮箱已被注册")
        current_user.email = user_data['email']
    
    # 更新密码
    if 'password' in user_data and user_data['password']:
        current_user.password_hash = get_password_hash(user_data['password'])
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "id": current_user.id,
        "phone": current_user.phone,
        "email": current_user.email,
        "nickname": current_user.nickname,
        "role": current_user.role.value,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }

@router.post("/change-password", tags=["认证"], summary="修改密码")
async def change_password(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    修改用户密码
    
    - **current_password**: 当前密码
    - **new_password**: 新密码
    
    需要在请求头中携带 Authorization: Bearer {token}
    """
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        raise HTTPException(status_code=400, detail="请提供当前密码和新密码")
    
    # 验证当前密码
    if not verify_password(current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="当前密码不正确")
    
    # 验证新密码强度
    validate_password(new_password)
    
    # 更新密码
    current_user.password_hash = get_password_hash(new_password)
    db.commit()
    
    return {"message": "密码修改成功"}

@router.post("/change-phone", tags=["认证"], summary="修改手机号")
async def change_phone(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    修改用户手机号
    
    - **current_password**: 当前密码（用于身份验证）
    - **new_phone**: 新手机号
    
    需要在请求头中携带 Authorization: Bearer {token}
    """
    current_password = data.get('current_password')
    new_phone = data.get('new_phone')
    
    if not current_password or not new_phone:
        raise HTTPException(status_code=400, detail="请提供当前密码和新手机号")
    
    # 验证当前密码
    if not verify_password(current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="当前密码不正确")
    
    # 检查新手机号是否已被其他用户使用
    existing_user = db.query(User).filter(
        User.phone == new_phone,
        User.id != current_user.id
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="手机号已被注册")
    
    # 更新手机号
    current_user.phone = new_phone
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "手机号修改成功",
        "phone": current_user.phone
    }
