# 面试模拟训练平台 - 部署指南

## 1. 环境要求

### 1.1 服务器要求
- **操作系统**: Linux (Ubuntu 20.04+ / CentOS 7+)
- **内存**: 至少 2GB RAM
- **磁盘空间**: 至少 10GB 可用空间
- **网络**: 公网 IP，开放 80/443 端口

### 1.2 依赖软件
- Python 3.10+
- pip
- Git
- Docker (可选，推荐)
- Docker Compose (可选，推荐)
- Nginx (可选，用于反向代理)

## 2. 部署方式

### 方式一：Docker 部署（推荐）

#### 2.1 安装 Docker 和 Docker Compose

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com | sh

# 安装 Docker Compose
sudo apt install docker-compose -y
```

#### 2.2 配置域名和 SSL

1. **修改配置文件**:
   - 编辑 `docker-compose.yml`，替换 `your-email@example.com` 和 `your-domain.com`
   - 编辑 `nginx.conf`，替换 `your-domain.com`

2. **获取 SSL 证书**:
```bash
# 创建证书目录
mkdir -p certbot/conf certbot/www

# 获取证书
docker-compose run --rm certbot
```

#### 2.3 启动服务

```bash
# 构建并启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f
```

#### 2.4 验证部署

访问 `https://your-domain.com` 查看应用是否正常运行。

### 方式二：直接部署（不推荐用于生产环境）

#### 2.1 克隆项目

```bash
git clone <repository-url>
cd msmlxfpt
```

#### 2.2 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 2.3 配置环境变量

```bash
# 复制并修改配置文件
cp .env.example .env

# 编辑 .env 文件，修改以下配置：
# - SECRET_KEY: 使用强随机密钥
# - DEBUG: 设置为 False
# - DATABASE_URL: 生产环境建议使用 PostgreSQL/MySQL
```

#### 2.4 生成安全密钥

```bash
# 生成随机密钥
python -c "import secrets; print(secrets.token_hex(32))"
```

将生成的密钥复制到 `.env` 文件中的 `SECRET_KEY` 字段。

#### 2.5 启动服务

```bash
# 使用 Uvicorn 启动（生产环境建议使用多进程）
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 3. 安全配置

### 3.1 密钥管理
- **SECRET_KEY**: 必须使用强随机字符串，切勿泄露
- **数据库密码**: 如果使用外部数据库，确保密码安全

### 3.2 HTTPS 配置
- 生产环境必须启用 HTTPS
- 使用 Let's Encrypt 免费证书
- 配置 SSL 证书自动续期

### 3.3 防火墙配置

```bash
# 允许 HTTP 和 HTTPS 流量
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 3.4 禁用调试模式
确保 `.env` 文件中 `DEBUG=False`

## 4. 数据库配置

### 4.1 SQLite（开发/测试环境）
```bash
# SQLite 无需额外配置，数据文件位于项目根目录
```

### 4.2 PostgreSQL（生产环境推荐）

修改 `.env` 文件：
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### 4.3 MySQL
```env
DATABASE_URL=mysql+pymysql://username:password@host:port/database_name
```

## 5. 初始化数据

```bash
# 初始化题库数据
python init_data.py

# 初始化数据库表（首次部署）
python init_db.py
```

## 6. 日志管理

### 6.1 Docker 日志

```bash
# 查看所有日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f app
```

### 6.2 应用日志

应用日志默认输出到控制台，可以配置输出到文件：

```bash
# 启动时重定向日志
uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
```

## 7. 监控和维护

### 7.1 健康检查

```bash
# 检查服务状态
curl http://localhost:8000/

# 检查 API 健康状态
curl http://localhost:8000/api/auth/me -H "Authorization: Bearer <token>"
```

### 7.2 备份数据库

```bash
# SQLite 备份
cp interview.db interview.db.backup

# PostgreSQL 备份
pg_dump -U username database_name > backup.sql

# MySQL 备份
mysqldump -u username -p database_name > backup.sql
```

### 7.3 更新部署

```bash
# 停止服务
docker-compose down

# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build
```

## 8. 性能优化

### 8.1 Uvicorn 配置
- 使用多进程模式（--workers 参数）
- 根据服务器 CPU 核心数设置 workers 数量（建议为 CPU 核心数 × 2）

### 8.2 启用 Gzip 压缩
在 Nginx 配置中添加：
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

### 8.3 配置 CDN
- 将静态资源托管到 CDN
- 配置浏览器缓存策略

## 9. 常见问题

### 9.1 端口被占用

```bash
# 查找占用端口的进程
sudo lsof -i :8000

# 杀死进程
sudo kill -9 <PID>
```

### 9.2 数据库连接失败

检查：
- 数据库服务是否运行
- 数据库配置是否正确
- 防火墙是否允许数据库端口

### 9.3 SSL 证书问题

确保：
- 域名已正确解析到服务器
- 80 端口未被其他服务占用
- 证书文件路径正确

## 10. 部署清单

- [ ] 服务器环境准备完成
- [ ] 域名已解析到服务器
- [ ] SSL 证书已配置
- [ ] 环境变量已正确配置（特别是 SECRET_KEY）
- [ ] 调试模式已关闭
- [ ] 数据库已初始化
- [ ] 防火墙规则已配置
- [ ] 日志记录已配置
- [ ] 备份策略已制定

---

**部署完成后**，访问 `https://your-domain.com` 即可使用面试模拟训练平台！
