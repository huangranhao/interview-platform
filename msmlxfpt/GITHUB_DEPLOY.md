# 面试模拟训练平台 - GitHub + Railway/Render 部署指南

## 📦 第一步：上传项目到 GitHub

### 1.1 初始化 Git 仓库

```bash
# 在项目根目录执行
cd d:\面试模拟训练平台\msmlxfpt

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Interview Platform"
```

### 1.2 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写仓库名称：`interview-platform`
3. 选择 Public 或 Private（推荐 Private）
4. 点击 **Create repository**

### 1.3 推送到 GitHub

```bash
# 关联远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/interview-platform.git

# 推送代码
git branch -M main
git push -u origin main
```

---

## 🚀 第二步：使用 Railway 部署（推荐）

### 2.1 注册 Railway

访问 https://railway.app 并注册账号（GitHub 登录即可）

### 2.2 创建新项目

1. 点击 **New Project**
2. 选择 **Deploy from GitHub repo**
3. 选择您的 `interview-platform` 仓库
4. 点击 **Deploy Now**

### 2.3 配置环境变量

在 Railway 项目中，添加以下环境变量：

```env
APP_ENV=production
DATABASE_URL=sqlite:///./interview.db
SECRET_KEY=（自动生成或使用：e71c12f8bb75c69ecb601d34bfe1e2032c5643076d85160abc00afb3615e96fd）
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
```

### 2.4 部署完成

Railway 会自动检测 `railway.toml` 并部署，等待 1-2 分钟即可访问。

Railway 会分配一个临时域名（如 `interview-platform.up.railway.app`）

---

## 🌟 第三步：使用 Render 部署（备选）

### 3.1 注册 Render

访问 https://render.com 并注册账号（GitHub 登录）

### 3.2 创建 Web Service

1. 点击 **New +** → **Web Service**
2. 选择您的 `interview-platform` 仓库
3. 填写配置：
   - **Name**: `interview-platform`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. 点击 **Create Web Service**

### 3.3 配置环境变量

在 Render Dashboard → Environment 中添加：

```env
APP_ENV=production
DATABASE_URL=sqlite:///./interview.db
SECRET_KEY=e71c12f8bb75c69ecb601d34bfe1e2032c5643076d85160abc00afb3615e96fd
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
```

---

## 🔗 第四步：绑定自定义域名

### 4.1 在 Railway 中绑定域名

1. 在 Railway 项目 → Settings → Domains
2. 点击 **Add Custom Domain**
3. 输入：`hrh01.abrdns.com`
4. Railway 会提供 CNAME 记录

### 4.2 在 DNS 管理中添加记录

回到您的域名管理面板（CloudDNS）：

添加 CNAME 记录：
- **主机名**: `@`
- **类型**: CNAME
- **指向**: Railway 提供的域名（如 `interview-platform.up.railway.app`）
- **TTL**: 自动或 600

### 4.3 启用 HTTPS

Railway 和 Render 都会自动提供免费 SSL 证书，无需额外配置。

---

## 📝 初始化题库数据

部署成功后，需要在平台内初始化题库数据：

**方法一：手动执行（推荐）**

1. 在 Railway/Render 的 Dashboard 中打开 **Shell**
2. 执行：
   ```bash
   python init_data.py
   ```

**方法二：通过 API**

访问平台后，注册账号测试功能，题库会自动加载。

---

## ✅ 验证部署

1. 访问您的临时域名或 `https://hrh01.abrdns.com`
2. 测试功能：
   - 注册账号
   - 登录
   - 浏览题库
   - 开始面试

---

## 🛠️ 常见问题

### Railway 部署失败

- 检查 `requirements.txt` 是否完整
- 查看 Railway 日志（项目 → Logs）
- 确保 `uvicorn` 在依赖列表中

### Render 部署失败

- 确认 `render.yaml` 在项目根目录
- 检查环境变量是否配置正确
- 查看 Render 日志（Dashboard → Logs）

### 数据库问题

Railway 和 Render 的免费计划支持 SQLite，但如果需要持久化存储，建议添加 PostgreSQL 数据库。

---

## 📞 获取帮助

部署过程中遇到问题？
- Railway 文档：https://docs.railway.app
- Render 文档：https://render.com/docs
- GitHub Issues（如果需要）
