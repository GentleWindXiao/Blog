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
- **部署**: Vercel

### 后端 (backend/)
- **框架**: Django + Django REST Framework
- **数据库**: PostgreSQL (生产) / SQLite (开发)
- **认证**: JWT / Session
- **跨域**: django-cors-headers
- **部署**: Render

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

# 部署后端 (Render)
# 前端部署到 Vercel
```

## 配置说明

### 环境变量

#### 后端环境变量 (env.example)
```env
# Django 配置
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库配置
DB_ENGINE=django.db.backends.postgresql
DB_NAME=blog_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# 邮件配置
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@blog.com
```

#### 前端环境变量 (env.example)
```env
# API配置
VITE_API_BASE_URL=http://localhost:8000/api
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

### Docker 部署
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

### 传统部署
1. 构建前端项目
2. 配置后端环境变量
3. 启动后端服务
4. 配置反向代理 (Nginx)

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
