from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 密码上下文 - 使用纯Python实现的pbkdf2_sha256方案
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_nickname() -> str:
    """生成随机昵称"""
    import random
    adjectives = ["勤奋的", "聪明的", "勇敢的", "乐观的", "自信的", "认真的", "专注的", "热情的"]
    nouns = ["程序员", "设计师", "产品经理", "运营", "工程师", "分析师", "架构师"]
    return f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(1000, 9999)}"

def calculate_score(answer: str, keywords: str) -> dict:
    """模拟AI评估打分"""
    import random
    
    # 简单的关键词匹配
    keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]
    matched_keywords = sum(1 for kw in keyword_list if kw.lower() in answer.lower())
    relevance = min(10, matched_keywords * 2 + random.uniform(0, 3))
    
    # 回答长度评分
    length_score = min(10, len(answer) / 50 * 10)
    
    # 流利度评分（模拟）
    fluency_score = random.uniform(6, 10)
    
    # 信心评分（模拟）
    confidence_score = random.uniform(5, 10)
    
    # 综合评分
    overall_score = (relevance * 0.3 + length_score * 0.2 + fluency_score * 0.25 + confidence_score * 0.25)
    
    return {
        "overall_score": round(overall_score, 2),
        "content_score": round(relevance, 2),
        "fluency_score": round(fluency_score, 2),
        "confidence_score": round(confidence_score, 2)
    }

def generate_suggestions(score: dict, question_content: str) -> str:
    """生成评估建议"""
    suggestions = []
    
    if score["content_score"] < 7:
        suggestions.append("回答内容需要更丰富，建议多结合具体案例说明。")
    if score["fluency_score"] < 7:
        suggestions.append("回答时可以放慢语速，保持平稳的节奏。")
    if score["confidence_score"] < 7:
        suggestions.append("建议增加眼神交流，保持自信的姿态。")
    
    if not suggestions:
        suggestions.append("回答表现良好，继续保持！")
    
    return "\n".join(suggestions)
