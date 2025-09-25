# Blog 项目

一个现代化的全栈博客系统，采用前后端分离架构。

## 项目结构

```
Blog/
├─ frontend/                    ← Vue.js 前端项目
│  ├─ src/
│  │  ├─ components/           ← Vue 组件
│  │  ├─ views/               ← 页面视图
│  │  ├─ router/              ← 路由配置
│  │  ├─ stores/              ← Pinia 状态管理
│  │  ├─ assets/              ← 静态资源
│  │  └─ utils/               ← 工具函数
│  ├─ public/                 ← 公共资源
│  ├─ package.json            ← 前端依赖
│  ├─ vite.config.js          ← Vite 配置
│  └─ index.html              ← 入口文件
├─ backend/                    ← Django 后端 API
│  ├─ blog_project/           ← Django 项目配置
│  │  ├─ settings.py          ← 项目设置
│  │  ├─ urls.py              ← 主路由
│  │  └─ wsgi.py              ← WSGI 配置
│  ├─ accounts/               ← 用户管理应用
│  ├─ posts/                  ← 文章管理应用
│  ├─ comments/               ← 评论管理应用
│  ├─ manage.py               ← Django 管理脚本
│  ├─ requirements.txt        ← Python 依赖
│  └─ env.example             ← 环境变量示例
└─ README.md
```

## 技术栈

### 前端 (frontend/)
- **框架**: Vue.js 3
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **样式**: CSS3 / SCSS
- **部署**: 阿里云 + 宝塔Linux

### 后端 (backend/)
- **框架**: Django + Django REST Framework
- **数据库**: MySQL (生产) / SQLite (开发)
- **认证**: JWT / Session
- **跨域**: django-cors-headers
- **部署**: 阿里云 + 宝塔Linux

## 功能特性

### 前端功能
- 📝 文章列表和详情页
- 🔍 文章搜索和分类
- 📱 响应式设计
- 🌙 深色/浅色主题切换
- 💬 评论系统
- 📊 文章统计
- 🏷️ 标签管理
- 📂 分类管理

### 后端功能
- 🔐 用户认证和授权
- 📄 文章CRUD操作
- 🏷️ 标签和分类管理
- 💬 评论系统
- 📁 文件上传
- 📊 数据统计
- 🔍 全文搜索
- 📧 邮件通知

## 快速开始

### 环境要求
- Node.js >= 16.0.0
- Python >= 3.8
- PostgreSQL (生产环境)

### 安装依赖

```bash
# 安装前端依赖
cd frontend
npm install

# 安装后端依赖
cd backend
pip install -r requirements.txt
```

### 开发环境启动

```bash
# 启动后端服务 (端口: 8000)
cd backend
python manage.py runserver

# 启动前端服务 (端口: 3000)
cd frontend
npm run dev
```

### 生产环境部署

```bash
# 构建前端
cd frontend
npm run build

# 部署到阿里云 + 宝塔Linux
# 详见部署指南章节
```

## 配置说明

### 环境变量

#### 后端环境变量 (env.example)
```env
# Django 配置
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

# 数据库配置 (阿里云RDS MySQL)
DB_ENGINE=django.db.backends.mysql
DB_NAME=blog_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your-rds-endpoint.aliyuncs.com
DB_PORT=3306

# Redis 配置 (阿里云Redis)
REDIS_URL=redis://your-redis-endpoint.aliyuncs.com:6379/0

# 邮件配置
EMAIL_HOST=smtp.aliyun.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=your-email@aliyun.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@your-domain.com
```

#### 前端环境变量 (env.example)
```env
# API配置
VITE_API_BASE_URL=https://your-domain.com/api
VITE_APP_TITLE=我的博客
VITE_APP_DESCRIPTION=一个现代化的博客系统
```

## API 接口

### 文章相关
- `GET /api/posts` - 获取文章列表
- `GET /api/posts/:id` - 获取文章详情
- `POST /api/posts` - 创建文章
- `PUT /api/posts/:id` - 更新文章
- `DELETE /api/posts/:id` - 删除文章

### 用户相关
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `GET /api/auth/profile` - 获取用户信息
- `PUT /api/auth/profile` - 更新用户信息

### 分类和标签
- `GET /api/categories` - 获取分类列表
- `GET /api/tags` - 获取标签列表

## 开发规范

### 代码规范
- 使用 ESLint 进行代码检查
- 使用 Prettier 进行代码格式化
- 遵循 Git Flow 工作流
- 编写单元测试和集成测试

### 提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动
```

## 部署

### 阿里云 + 宝塔Linux 部署

> 📖 **详细部署指南**: 请参考 [DEPLOYMENT_BT.md](DEPLOYMENT_BT.md) 获取完整的宝塔Linux部署指南。

#### 快速开始

1. **服务器准备**
   - 购买阿里云ECS服务器（推荐2核4G）
   - 安装宝塔Linux面板
   - 安装必要软件：Nginx, Python 3.8+, PostgreSQL, Redis, Node.js

2. **后端部署**
   - 创建Python项目
   - 上传代码并安装依赖
   - 配置环境变量和数据库
   - 启动Gunicorn服务

3. **前端部署**
   - 构建前端项目
   - 配置Nginx反向代理
   - 设置SSL证书

4. **进程守护**
   - 配置宝塔进程守护
   - 设置开机自启

#### 环境要求

- **服务器**: 阿里云ECS (2核4G内存，40G系统盘)
- **操作系统**: CentOS 7.x 或 Ubuntu 20.04 LTS
- **Web服务器**: Nginx 1.20+
- **数据库**: MySQL 8.0+ (或阿里云RDS)
- **缓存**: Redis 6.0+ (或阿里云Redis)
- **编程语言**: Python 3.8+, Node.js 16+

### Docker 部署（开发环境）

后端已提供完整的 Docker 配置，位于 `backend/` 目录：

- `backend/.dockerignore`: 精简构建上下文
- `backend/Dockerfile`: 构建 Django 应用镜像
- `backend/entrypoint.sh`: 容器启动脚本（等待数据库、迁移、启动 Gunicorn）
- `backend/gunicorn.conf.py`: Gunicorn 配置
- `backend/docker-compose.yml`: 本地/服务器一键启动（包含 Postgres）

使用方法：

```bash
# 进入后端目录
cd backend

# 准备环境变量（可直接复制 env.example）
copy env.example .env   # Windows PowerShell 使用：Copy-Item env.example .env

# 构建并启动（首次会拉取 Postgres）
docker-compose up -d --build

# 查看日志
docker-compose logs -f --tail 100

# 停止并移除
docker-compose down
```

默认对外暴露端口：
- 应用服务：`http://localhost:8000`
- 数据库：`localhost:3306`（用户名/密码：`root/root`）

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目链接: [https://github.com/GentleWindXiao/Blog](https://github.com/GentleWindXiao/Blog)
- 问题反馈: [https://github.com/GentleWindXiao/Blog/issues](https://github.com/GentleWindXiao/Blog/issues)

---

## 🤖 AI 生成说明

> **本项目由 AI 辅助生成**
> 
> 本项目的基础架构、项目结构、配置文件等均由 AI 助手协助创建，包括：
> - Vue.js 前端项目脚手架搭建
> - Django 后端项目架构设计
> - 前后端分离配置
> - 开发环境配置
> - 部署架构规划
> 
> 具体功能实现和业务逻辑由开发者完成。

---

⭐ 如果这个项目对你有帮助，请给它一个星标！
