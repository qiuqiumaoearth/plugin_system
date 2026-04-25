# 项目结构说明

本文档描述了插件化执行系统的完整目录结构。

## 根目录结构

```
plugin-execution-system/
├── v2/                          # v2.0 主版本实现
├── docs/                        # 项目文档
├── .git/                        # Git 版本控制
├── .gitignore                   # Git 忽略文件配置
├── CHANGELOG.md                 # 版本变更日志
├── CONTRIBUTING.md              # 贡献指南
├── LICENSE                      # MIT 许可证
├── README.md                    # 项目主文档（中文）
└── README_EN.md                 # 项目主文档（英文）
```

## v2/ 目录（当前版本）

```
v2/
├── api/                         # API 网关层
│   ├── http_server.py           # HTTP 服务器
│   ├── middleware/              # 中间件
│   └── routes/                  # 路由定义
│
├── config/                      # 配置文件
│   └── system.yaml              # 系统配置
│
├── core/                        # 核心框架
│   ├── adapters/                # 多语言适配器
│   ├── base.py                  # 插件基类定义
│   ├── context.py               # 执行上下文
│   ├── execution/               # 执行层
│   │   ├── executor.py          # 插件执行器
│   │   └── scheduler.py         # 调度器
│   ├── management/              # 管理层
│   │   ├── config.py            # 配置管理
│   │   ├── lifecycle.py         # 生命周期管理
│   │   ├── loader.py            # 插件加载器
│   │   └── registry.py          # 插件注册表
│   ├── observability/           # 可观测层
│   │   ├── logger.py            # 日志系统
│   │   └── metrics.py           # 指标采集
│   ├── orchestration/           # 编排层
│   └── utils/                   # 工具函数
│
├── plugins/                     # 插件目录
│   ├── builtin/                 # 内置插件
│   │   ├── echo_plugin.py       # 回显插件
│   │   ├── sum_plugin.py        # 求和插件
│   │   └── validator_plugin.py  # 验证插件
│   └── external/                # 外部插件（用户自定义）
│       └── .gitkeep
│
├── storage/                     # 存储目录
│   ├── logs/                    # 日志文件
│   ├── data/                    # 数据文件
│   ├── cache/                   # 缓存文件
│   └── .gitkeep
│
├── tests/                       # 测试
│   ├── test_*.py                # 单元测试
│   └── integration/             # 集成测试
│
├── examples/                    # 示例代码
│   └── basic_usage.py           # 基础使用示例
│
├── docs/                        # v2 详细文档
│   └── quickstart.md            # 快速开始
│
├── scripts/                     # 脚本工具
│
├── Dockerfile                   # Docker 镜像构建
├── docker-compose.yml           # Docker Compose 配置
├── main.py                      # 主程序入口
├── requirements.txt             # Python 依赖
├── PROJECT_REPORT.md            # 项目报告
├── PROJECT_SUMMARY.md           # 项目摘要
└── README.md                    # v2 版本说明
```

## docs/ 目录（项目文档）

```
docs/
├── design/                      # 设计文档
│   ├── v1-design.md             # v1 版本设计方案
│   └── v2-design.md             # v2 版本设计方案
│
├── architecture.md              # 架构设计（待创建）
├── plugin-development.md        # 插件开发指南（待创建）
├── api-reference.md             # API 参考（待创建）
├── deployment.md                # 部署指南（待创建）
└── FAQ.md                       # 常见问题（待创建）
```

## 核心模块说明

### 1. core/ - 核心框架

- **base.py**: 定义插件基类和接口规范
- **management/**: 插件管理相关功能
  - loader.py: 动态加载插件
  - registry.py: 维护插件注册表
  - lifecycle.py: 管理插件生命周期
  - config.py: 配置管理
- **execution/**: 插件执行相关功能
  - executor.py: 执行插件并处理异常
  - scheduler.py: 调度插件执行
- **observability/**: 可观测性功能
  - logger.py: 结构化日志
  - metrics.py: 指标采集
- **orchestration/**: 工作流编排
- **adapters/**: 多语言插件适配器

### 2. plugins/ - 插件目录

- **builtin/**: 系统内置插件
- **external/**: 用户自定义插件（不纳入版本控制）

### 3. api/ - API 网关

- HTTP/gRPC 接口
- 中间件（认证、限流等）
- 路由定义

### 4. config/ - 配置

- 系统配置文件
- 插件配置文件

### 5. storage/ - 存储

- logs/: 日志文件
- data/: 数据文件
- cache/: 缓存文件

## 文件命名规范

- **Python 文件**: snake_case (如 `plugin_loader.py`)
- **类名**: PascalCase (如 `PluginLoader`)
- **配置文件**: kebab-case.yaml (如 `system-config.yaml`)
- **文档文件**: kebab-case.md (如 `plugin-development.md`)

## 版本管理

- **v2/**: 当前主版本（v2.0.0）
- **docs/design/**: 历史版本设计文档归档
- 未来版本将以 v3/, v4/ 等形式组织

## 忽略文件

以下文件/目录不纳入版本控制（见 .gitignore）：

- `__pycache__/`, `*.pyc`: Python 编译文件
- `venv/`, `.venv/`: 虚拟环境
- `v2/storage/logs/*`: 日志文件
- `v2/storage/data/*`: 数据文件
- `v2/storage/cache/*`: 缓存文件
- `v2/plugins/external/*`: 外部插件
- `.vscode/`, `.idea/`: IDE 配置

## 扩展指南

### 添加新插件

1. 在 `v2/plugins/builtin/` 或 `v2/plugins/external/` 创建插件文件
2. 继承 `PluginBase` 类
3. 实现必要方法
4. 系统自动发现并加载

### 添加新文档

1. 在 `docs/` 目录创建 Markdown 文件
2. 更新主 README.md 中的文档链接

### 添加新测试

1. 在 `v2/tests/` 目录创建测试文件
2. 使用 pytest 框架编写测试

## 相关文档

- [主 README](../README.md)
- [v2 版本说明](../v2/README.md)
- [贡献指南](../CONTRIBUTING.md)
- [变更日志](../CHANGELOG.md)
