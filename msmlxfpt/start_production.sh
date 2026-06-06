#!/bin/bash
# 面试模拟训练平台 - 生产环境启动脚本

# 设置环境变量
export APP_ENV=production

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 运行应用
echo "启动生产服务器..."
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
