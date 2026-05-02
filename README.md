# NCMDB - 园区网网络资产管理系统

<div align="center">

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Django](https://img.shields.io/badge/django-5.2.8-red.svg)
![Vue](https://img.shields.io/badge/vue-3.5-brightgreen.svg)
![Node](https://img.shields.io/badge/node-22.04+-orange.svg)

**N**etwork + **CMDB** = **NCMDB** | 基于实际网络运维实习经验开发的毕业设计项目

[功能特性](#-功能特性) • [技术栈](#-技术栈) • [快速开始](#-快速开始) • [项目结构](#-项目结构) • [API文档](#-api文档) • [部署说明](#-部署说明) • [贡献指南](#-贡献指南)

</div>

---

## 📋 项目简介

**NCMDB**（Network Configuration Management Database）是一个面向园区网的综合网络资产管理系统。

- **N** = Network（网络）：专注于网络设备、IP地址、终端等网络资源管理
- **CMDB** = Configuration Management Database（配置管理数据库）：提供完整的资产配置信息管理

本项目为软件工程专业毕业设计作品，结合真实的网络运维实习经历开发，旨在解决传统网络运维中的痛点问题，提供设备管理、故障报修、巡检管理、库存管理等一体化解决方案。

### 🎯 设计目标

- **统一管理**：整合网络设备、基础设施、库存备件等多维度资源
- **流程规范**：标准化故障报修、工单处理、巡检执行等运维流程
- **移动优先**：支持 PC 端和移动端双平台，满足现场运维需求
- **数据驱动**：通过告警聚合、统计分析辅助运维决策

---

## ✨ 功能特性

### 🔧 核心模块

#### 1. 用户与权限管理
- 基于角色的访问控制（RBAC）
- JWT Token 认证
- 自定义用户模型，支持网络工程师标识

#### 2. 设备管理（CMDB）
- **网络设备管理**：交换机、路由器、防火墙、无线AP等设备的完整信息记录
- **IP地址管理（IPAM）**：IP段划分、DHCP范围、保留地址、VLAN关联
- **终端信息管理**：办公终端的IP/MAC/VLAN绑定记录
- **设备维保跟踪**：维保起止日期提醒

#### 3. 基础设施管理
- 机房信息管理
- 机柜管理与设备上架
- 基础设施设备管理（空调、UPS等）
- 设备连接关系拓扑

#### 4. 故障报修工单系统
- 工单自动生成（6位数字编号）
- 多级紧急程度（低/一般/高/紧急）
- 工单状态流转：待受理 → 已受理 → 处理中 → 已解决 → 已完成
- 处理记录全程追溯
- 满意度评价（1-5星）

#### 5. 运维事务管理
- **巡检计划**：定期巡检任务制定
- **巡检任务**：任务执行与结果记录
- 巡检报告生成

#### 6. 库存管理
- 备品备件出入库管理
- 库存记录追踪
- 库存盘点功能

#### 7. 告警管理
- Zabbix Webhook 告警接收
- 告警分类与过滤
- 告警通知推送

#### 8. 文件管理
- 变更日志归档
- 巡检记录附件
- 系统工具下载
- 资产台账导出

#### 9. 联系人管理
- 运维团队联系信息
- 厂商技术支持联系方式

---

## 🛠️ 技术栈

### 后端（ncmdb-server）
| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 编程语言（推荐3.10） |
| Django | 5.2.8 | Web框架 |
| Django REST Framework | 3.16.1 | API框架 |
| SimpleJWT | 5.5.1 | JWT认证 |
| SQLite / MySQL | 3.x / 5.7+ | 数据库（默认SQLite，推荐MySQL） |
| django-simpleui | 2025.6.24 | 管理后台UI美化 |
| django-cors-headers | 4.9.0 | 跨域支持 |
| django-filter | 25.2 | API过滤 |
| PyZabbix | 1.3.1 | Zabbix集成 |
| Pandas | 2.3.3 | 数据处理 |
| python-decouple | 3.8 | 环境变量管理 |

### 前端（ncmdb-view - PC端）
| 技术 | 版本 | 说明 |
|------|------|------|
| Vue 3 | 3.5.24 | 渐进式JavaScript框架 |
| Vite | 7.2.4 | 下一代前端构建工具 |
| Element Plus | 2.11.8 | Vue 3组件库 |
| Pinia | 3.0.4 | Vue状态管理 |
| Vue Router | 4.6.3 | 路由管理 |
| Axios | 1.13.2 | HTTP客户端 |
| ECharts | 6.0.0 | 数据可视化 |
| XLSX | 0.18.5 | Excel导出 |

### 移动端（netms-mobile）
| 技术 | 版本 | 说明 |
|------|------|------|
| Vue 3 | 3.5.18 | 渐进式JavaScript框架 |
| Vite | 7.1.2 | 前端构建工具 |
| Element Plus | 2.11.2 | 移动端适配组件库 |
| Pinia | 3.0.4 | 状态管理 |
| Vue Router | 4.5.1 | 路由管理 |
| Axios | 1.12.2 | HTTP客户端 |
| Sass | 1.93.2 | CSS预处理器 |

---

## 🚀 快速开始

### 前置要求

- **Python 3.10+**（推荐使用Python 3.10）
- **Node.js 22.04+**（推荐使用LTS版本）
- **SQLite 3.x**（默认数据库，无需额外配置）
- **MySQL 5.7+ 或 8.0**（可选，生产环境推荐）
- Git

### 1. 克隆项目

```bash
git clone https://github.com/dingtongbin/ncmdb.git
cd ncmdb
```

### 2. 后端配置

#### 安装依赖

```bash
cd ncmdb-server
pip install -r requirements.txt
```

#### 数据库配置

**方案一：使用SQLite（默认，推荐开发环境）**

项目默认配置使用SQLite数据库，无需额外配置即可运行。数据库文件将自动创建在项目根目录。

如需显式配置，在 `setting/settings.py` 中已注释了SQLite配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**方案二：使用MySQL（推荐生产环境）**

1. 确保已安装MySQL并创建数据库：
```sql
CREATE DATABASE ncmdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 在项目根目录创建 `.env` 文件：
```env
DB_NAME=ncmdb
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

3. 确保 `setting/settings.py` 中使用MySQL配置（已默认配置）：
```python
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

> 💡 **提示**：从SQLite迁移到MySQL时，可使用Django的dumpdata和loaddata命令进行数据迁移。

#### 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 创建超级用户

```bash
python manage.py createsuperuser
```

#### 启动后端服务

```bash
python manage.py runserver 8000
```

访问管理后台：`http://localhost:8000/admin`

### 3. 前端配置（PC端）

```bash
cd ncmdb-view
npm install
npm run dev
```

访问前端页面：`http://localhost:5173`

### 4. 移动端配置

```bash
cd netms-mobile
npm install
npm run dev
```

访问移动端：`http://localhost:5174`

---

## 📁 项目结构

```
ncmdb/
├── ncmdb-server/                 # 后端服务
│   ├── alert/                    # 告警管理模块
│   ├── contact/                  # 联系人管理模块
│   ├── device/                   # 设备管理模块（CMDB）
│   ├── file_management/          # 文件管理模块
│   ├── integrated_facility/      # 基础设施管理模块
│   ├── inventory/                # 库存管理模块
│   ├── operation_affairs/        # 运维事务模块
│   ├── repair/                   # 故障报修模块
│   ├── user/                     # 用户管理模块
│   ├── setting/                  # Django配置
│   │   ├── settings.py           # 项目配置
│   │   ├── urls.py               # 路由配置
│   │   └── wsgi.py               # WSGI入口
│   ├── media/                    # 媒体文件存储
│   ├── manage.py                 # Django管理脚本
│   ├── requirements.txt          # Python依赖
│   └── .env                      # 环境变量配置
│
├── ncmdb-view/                   # PC端前端
│   ├── src/
│   │   ├── api/                  # API接口封装
│   │   ├── components/           # 公共组件
│   │   ├── view/                 # 页面视图
│   │   ├── pinia/                # 状态管理
│   │   ├── router.js             # 路由配置
│   │   └── main.js               # 入口文件
│   ├── package.json              # 项目依赖
│   └── vite.config.js            # Vite配置
│
├── netms-mobile/                 # 移动端前端
│   ├── src/
│   │   ├── api/                  # API接口
│   │   ├── components/           # 组件
│   │   ├── view/                 # 页面
│   │   ├── router/               # 路由
│   │   ├── pinia/                # 状态管理
│   │   └── utils/                # 工具函数
│   ├── package.json              # 项目依赖
│   └── .env.development          # 开发环境配置
│
└── README.md                     # 项目说明文档
```

---

## 📖 API文档

### 认证接口

#### 登录获取Token
```http
POST /api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "your_password"
}
```

#### 刷新Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

### 主要API端点

| 模块 | 基础路径 | 说明 |
|------|---------|------|
| 用户 | `/api/user/` | 用户CRUD、权限管理 |
| 网络设备 | `/api/device/network-device/` | 设备增删改查 |
| IPAM | `/api/device/ipam/` | IP地址管理 |
| 终端 | `/api/device/terminal/` | 终端信息管理 |
| 工单 | `/api/repair/work-order/` | 工单管理 |
| 工单处理 | `/api/repair/work-order-handle-log/` | 处理记录 |
| 工单评价 | `/api/repair/work-order-evaluation/` | 满意度评价 |
| 巡检计划 | `/api/operation-affairs/patrol-plan/` | 巡检计划 |
| 巡检任务 | `/api/operation-affairs/patrol-task/` | 巡检任务 |
| 库存物品 | `/api/inventory/inventory-item/` | 库存管理 |
| 机房 | `/api/integrated-facility/equipment-room/` | 机房管理 |
| 机柜 | `/api/integrated-facility/rack/` | 机柜管理 |
| 告警 | `/api/alert/alert/` | 告警查询 |
| Webhook | `/api/alert/webhook-receiver/` | 告警接收 |

所有API请求需在Header中携带Token：
```http
Authorization: Bearer <your_access_token>
```

---

## 🌐 部署说明

### 生产环境部署

#### 后端部署（Nginx + Gunicorn）

1. 安装Gunicorn：
```bash
pip install gunicorn
```

2. 创建 `gunicorn_config.py`：
```python
bind = "0.0.0.0:8000"
workers = 4
timeout = 120
accesslog = "/var/log/ncmdb/gunicorn_access.log"
errorlog = "/var/log/ncmdb/gunicorn_error.log"
```

3. 启动服务：
```bash
gunicorn -c gunicorn_config.py setting.wsgi:application
```

4. Nginx配置：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/ncmdb-server/static/;
    }

    location /media/ {
        alias /path/to/ncmdb-server/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 前端部署

1. 构建生产版本：
```bash
cd ncmdb-view
npm run build

cd ../netms-mobile
npm run build
```

2. 将 `dist` 目录部署到Nginx：
```nginx
server {
    listen 80;
    server_name pc.your-domain.com;
    root /path/to/ncmdb-view/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}

server {
    listen 80;
    server_name mobile.your-domain.com;
    root /path/to/netms-mobile/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### Docker部署（可选）

创建 `Dockerfile`（后端）：
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "setting.wsgi:application"]
```

---

## 📸 系统截图

> 此处可添加系统界面截图展示

- 登录页面
- 设备管理界面
- 工单列表
- 移动端首页

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

请确保：
- 代码符合PEP 8规范（Python）
- 遵循Vue 3组合式API最佳实践
- 添加必要的测试用例
- 更新相关文档

---

## 📝 开发规范

### 后端规范
- 遵循Django官方编码规范
- Model字段使用中文verbose_name
- API返回统一JSON格式
- 使用DRF Serializer进行数据验证

### 前端规范
- 使用Vue 3 `<script setup>` 语法
- 组件名采用 PascalCase
- API调用统一在 `src/api/` 目录管理
- 使用Pinia进行状态管理

---

## 📄 许可证

本项目采用 Apache License 2.0 开源许可证。详见 [LICENSE](LICENSE) 文件。

```
Copyright 2026 dingtongbin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## 👨‍🎓 关于作者

**软件工程毕业设计项目**

本项目基于作者在园区网网络运维岗位的实习经历开发，旨在将实际运维工作中的痛点和需求转化为系统化的解决方案。

项目名称 **NCMDB** 的含义：
- **N** (Network) - 网络：聚焦园区网网络设备、IP地址、终端等网络资源
- **CMDB** (Configuration Management Database) - 配置管理数据库：提供完整的资产配置信息管理能力

- 📧 Email: dingtongbin@example.com
- 💼 GitHub: [@dingtongbin](https://github.com/dingtongbin)

---

## 🙏 致谢

感谢以下开源项目：

- [Django](https://www.djangoproject.com/)
- [Vue.js](https://vuejs.org/)
- [Element Plus](https://element-plus.org/)
- [ECharts](https://echarts.apache.org/)

---

## 📞 联系方式

如有问题或建议，欢迎：
- 提交 [Issue](https://github.com/dingtongbin/ncmdb/issues)
- 发送邮件至：dingtongbin@example.com

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给个Star！**

Made with ❤️ by [dingtongbin](https://github.com/dingtongbin)

</div>
