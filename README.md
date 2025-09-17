# Blog 项目

一个现代化的全栈博客系统，采用前后端分离架构。

## 项目结构

```
Blog/
├─ frontend/       ← Vue/Nuxt 或 VuePress/VitePress 前端项目
├─ backend/        ← Express/Node.js 后端 API
└─ README.md
```

## 技术栈

### 前端 (frontend/)
- **框架**: Vue.js / Nuxt.js / VuePress / VitePress
- **构建工具**: Vite / Webpack
- **UI框架**: Element Plus / Ant Design Vue / Vuetify
- **状态管理**: Pinia / Vuex
- **路由**: Vue Router
- **样式**: CSS3 / SCSS / Tailwind CSS

### 后端 (backend/)
- **运行时**: Node.js
- **框架**: Express.js
- **数据库**: MongoDB / MySQL / PostgreSQL
- **ORM/ODM**: Mongoose / Sequelize / Prisma
- **认证**: JWT / Passport.js
- **文件上传**: Multer
- **API文档**: Swagger / OpenAPI

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
- npm >= 8.0.0 或 yarn >= 1.22.0
- MongoDB / MySQL / PostgreSQL (根据后端配置)

### 安装依赖

```bash
# 安装前端依赖
cd frontend
npm install

# 安装后端依赖
cd ../backend
npm install
```

### 开发环境启动

```bash
# 启动后端服务 (端口: 3000)
cd backend
npm run dev

# 启动前端服务 (端口: 3001)
cd frontend
npm run dev
```

### 生产环境部署

```bash
# 构建前端
cd frontend
npm run build

# 启动后端生产服务
cd backend
npm start
```

## 配置说明

### 环境变量

#### 后端环境变量 (.env)
```env
# 服务器配置
PORT=3000
NODE_ENV=development

# 数据库配置
DB_HOST=localhost
DB_PORT=27017
DB_NAME=blog_db
DB_USER=your_username
DB_PASSWORD=your_password

# JWT配置
JWT_SECRET=your_jwt_secret
JWT_EXPIRES_IN=7d

# 文件上传配置
UPLOAD_PATH=./uploads
MAX_FILE_SIZE=5242880

# 邮件配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_password
```

#### 前端环境变量 (.env)
```env
# API配置
VITE_API_BASE_URL=http://localhost:3000/api
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

- 项目链接: [https://github.com/yourusername/blog](https://github.com/yourusername/blog)
- 问题反馈: [https://github.com/yourusername/blog/issues](https://github.com/yourusername/blog/issues)

---

⭐ 如果这个项目对你有帮助，请给它一个星标！
