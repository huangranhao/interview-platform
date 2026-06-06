@echo off
chcp 65001
echo ==========================================
echo     面试模拟训练平台 - 启动脚本
echo ==========================================

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt

REM 初始化数据库
echo 初始化数据库...
python init_db.py

REM 启动服务
echo 启动服务...
echo 服务地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo 按 Ctrl+C 停止服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
