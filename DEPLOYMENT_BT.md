# 宝塔Linux部署指南

本指南详细说明如何在阿里云ECS服务器上使用宝塔Linux面板部署Blog项目。

## 目录

- [服务器准备](#服务器准备)
- [宝塔面板安装](#宝塔面板安装)
- [环境配置](#环境配置)
- [后端部署](#后端部署)
- [前端部署](#前端部署)
- [域名和SSL配置](#域名和ssl配置)
- [进程守护](#进程守护)
- [监控和维护](#监控和维护)
- [故障排除](#故障排除)

## 服务器准备

### 1. 购买阿里云ECS服务器

**推荐配置：**
- CPU: 2核
- 内存: 4GB
- 系统盘: 40GB SSD
- 操作系统: CentOS 7.x 或 Ubuntu 20.04 LTS
- 带宽: 3-5Mbps

**安全组配置：**
- 开放端口: 22 (SSH), 80 (HTTP), 443 (HTTPS), 8000 (后端API)
- 允许来源: 0.0.0.0/0 (根据需要调整)

### 2. 连接服务器

```bash
# 使用SSH连接服务器
ssh root@your-server-ip
```

## 宝塔面板安装

### CentOS 7.x 安装

```bash
# 安装宝塔Linux面板
yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh ed8484bec
```

### Ubuntu 20.04 安装

```bash
# 安装宝塔Linux面板
wget -O install.sh http://download.bt.cn/install/install-ubuntu_6.0.sh && sudo bash install.sh ed8484bec
```

### 安装完成后

1. 记录面板地址、用户名和密码
2. 在浏览器中访问面板地址
3. 首次登录会提示安装LNMP环境

## 环境配置

### 1. 安装必要软件

在宝塔面板中安装以下软件：

**Web服务器：**
- Nginx 1.20+

**数据库：**
- MySQL 8.0+ (或使用阿里云RDS)

**缓存：**
- Redis 6.0+ (或使用阿里云Redis)

**编程语言：**
- Python 3.8+
- Node.js 16+

### 2. 创建数据库

**方式一：使用宝塔面板MySQL**
1. 进入数据库管理
2. 创建数据库：`blog_db`
3. 创建用户：`blog_user`
4. 记录连接信息

**方式二：使用阿里云RDS MySQL**
1. 在阿里云控制台创建RDS MySQL实例
2. 创建数据库和用户
3. 配置白名单（添加ECS公网IP）
4. 记录连接信息

### 3. 配置Redis

**方式一：使用宝塔面板Redis**
1. 进入软件商店
2. 安装Redis
3. 启动服务

**方式二：使用阿里云Redis**
1. 在阿里云控制台创建Redis实例
2. 配置白名单
3. 记录连接信息

## 后端部署

### 1. 创建Python项目

1. 进入宝塔面板
2. 点击"网站" → "添加站点"
3. 选择"Python项目"
4. 项目名称：`blog-backend`
5. 项目路径：`/www/wwwroot/blog-backend`
6. Python版本：3.8+

### 2. 上传代码

```bash
# 进入项目目录
cd /www/wwwroot/blog-backend

# 克隆代码（替换为你的仓库地址）
git clone https://github.com/your-username/Blog.git .

# 或者上传代码包并解压
```

### 3. 安装依赖

```bash
# 激活虚拟环境
source venv/bin/activate

# 安装Python依赖
pip install -r backend/requirements.txt

# 如果虚拟环境不存在，创建它
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 4. 配置环境变量

```bash
# 复制环境变量文件
cp backend/env.example backend/.env

# 编辑环境变量
nano backend/.env
```

**环境变量配置示例：**

```env
# Django 配置
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

# 数据库配置
DB_ENGINE=django.db.backends.mysql
DB_NAME=blog_db
DB_USER=blog_user
DB_PASSWORD=your-db-password
DB_HOST=your-db-host
DB_PORT=3306

# Redis 配置
REDIS_URL=redis://your-redis-host:6379/0

# 邮件配置
EMAIL_HOST=smtp.aliyun.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=your-email@aliyun.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@your-domain.com
```

### 5. 数据库迁移

```bash
# 进入后端目录
cd backend

# 激活虚拟环境
source ../venv/bin/activate

# 执行数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic --noinput
```

### 6. 测试启动

```bash
# 测试Django应用
python manage.py runserver 0.0.0.0:8000

# 如果正常，使用Gunicorn启动
gunicorn --config gunicorn.conf.py blog_project.wsgi:application
```

## 前端部署

### 1. 构建前端项目

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 构建生产版本
npm run build
```

### 2. 配置Nginx

1. 在宝塔面板中添加站点
2. 域名：`your-domain.com`
3. 根目录：`/www/wwwroot/blog-frontend/dist`

### 3. 配置反向代理

在站点配置中添加以下Nginx配置：

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # 前端静态文件
    location / {
        root /www/wwwroot/blog-frontend/dist;
        try_files $uri $uri/ /index.html;
        index index.html;
    }
    
    # API代理到后端
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # 静态文件缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 域名和SSL配置

### 1. 域名解析

在域名服务商处添加A记录：
- 记录类型：A
- 主机记录：@ 和 www
- 记录值：服务器公网IP

### 2. SSL证书配置

**方式一：Let's Encrypt免费证书**
1. 在宝塔面板中点击"SSL"
2. 选择"Let's Encrypt"
3. 填写域名和邮箱
4. 点击申请

**方式二：阿里云SSL证书**
1. 在阿里云控制台申请SSL证书
2. 下载证书文件
3. 在宝塔面板中上传证书

### 3. 强制HTTPS

在Nginx配置中添加：

```nginx
# HTTP重定向到HTTPS
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS配置
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL证书配置
    ssl_certificate /path/to/your/cert.pem;
    ssl_certificate_key /path/to/your/key.pem;
    
    # 其他配置...
}
```

## 进程守护

### 1. 配置进程守护

1. 进入宝塔面板
2. 点击"计划任务" → "进程守护"
3. 添加守护进程

**配置参数：**
- 名称：`blog-backend`
- 启动命令：`/www/wwwroot/blog-backend/venv/bin/gunicorn --config /www/wwwroot/blog-backend/backend/gunicorn.conf.py /www/wwwroot/blog-backend/backend/blog_project/wsgi:application`
- 工作目录：`/www/wwwroot/blog-backend/backend`
- 运行用户：`www`

### 2. 开机自启

确保进程守护设置为开机自启。

## 监控和维护

### 1. 日志监控

**后端日志：**
```bash
# 查看Gunicorn日志
tail -f /www/wwwroot/blog-backend/logs/gunicorn.log

# 查看Django日志
tail -f /www/wwwroot/blog-backend/logs/django.log
```

**Nginx日志：**
```bash
# 访问日志
tail -f /www/wwwlogs/your-domain.com.log

# 错误日志
tail -f /www/wwwlogs/your-domain.com.error.log
```

### 2. 性能监控

在宝塔面板中监控：
- CPU使用率
- 内存使用率
- 磁盘使用率
- 网络流量

### 3. 定期维护

**数据库备份：**
```bash
# 创建备份脚本
#!/bin/bash
pg_dump -h localhost -U blog_user blog_db > /backup/blog_$(date +%Y%m%d_%H%M%S).sql
```

**日志清理：**
```bash
# 清理旧日志
find /www/wwwlogs -name "*.log" -mtime +30 -delete
```

## 故障排除

### 1. 常见问题

**问题1：502 Bad Gateway**
- 检查后端服务是否启动
- 检查端口配置是否正确
- 查看Nginx错误日志

**问题2：数据库连接失败**
- 检查数据库服务状态
- 验证连接参数
- 检查防火墙设置

**问题3：静态文件404**
- 检查文件路径
- 验证Nginx配置
- 检查文件权限

### 2. 调试命令

```bash
# 检查端口占用
netstat -tlnp | grep :8000

# 检查进程状态
ps aux | grep gunicorn

# 检查Nginx配置
nginx -t

# 重启服务
systemctl restart nginx
```

### 3. 联系支持

如果遇到无法解决的问题，可以：
1. 查看宝塔面板日志
2. 检查阿里云控制台
3. 查看项目GitHub Issues

---

## 总结

通过本指南，您应该能够成功在阿里云ECS服务器上使用宝塔Linux面板部署Blog项目。记住定期备份数据，监控系统性能，并及时更新软件版本以确保系统安全稳定运行。
