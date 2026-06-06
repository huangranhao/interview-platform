from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 导入数据库模块和模型
from app.database import engine, Base
from app import models

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 导入路由
from app.routes import auth, interview, questions, assessment, resume

# 导入错误处理器
from app.middleware.error_handler import register_error_handlers

# 创建应用实例
app = FastAPI(
    title="面试模拟训练平台",
    version="1.0.0",
    description="AI驱动的面试模拟训练平台",
    docs_url=None,
    redoc_url=None
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(interview.router, prefix="/api/interview", tags=["面试"])
app.include_router(questions.router, prefix="/api/questions", tags=["题库"])
app.include_router(assessment.router, prefix="/api/assessment", tags=["评估"])
app.include_router(resume.router, prefix="/api/resume", tags=["简历"])

# 注册错误处理器
register_error_handlers(app)

# 配置模板
current_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "app", "templates"))

# 首页
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    """首页 - 简洁的按键式界面"""
    return templates.TemplateResponse("index.html", {"request": request})
