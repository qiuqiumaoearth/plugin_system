# Plugin Execution System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

企业级插件化执行系统，支持高并发、高可用、可观测、可扩展的插件管理与执行框架。

[English](README_EN.md) | 简体中文

## 📋 目录

- [特性](#特性)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [版本说明](#版本说明)
- [文档](#文档)
- [开发指南](#开发指南)
- [贡献](#贡献)
- [许可证](#许可证)

## ✨ 特性

### 核心能力

- 🔌 **统一插件接口** - 标准化的插件开发规范
- 🔄 **动态加载** - 支持插件热加载与热卸载
- 🎯 **生命周期管理** - 完整的插件生命周期钩子
- 🔗 **依赖解析** - 自动处理插件间依赖关系
- ⚡ **并发执行** - 支持串行/并行/异步执行模式
- 🛡️ **异常隔离** - 插件故障不影响系统稳定性

### 企业级特性

- 📊 **可观测性** - 结构化日志、指标采集、分布式追踪
- 🔐 **安全隔离** - 进程级隔离、资源配额、权限管理
- 🌐 **多语言支持** - Python/Go/JavaScript/Rust 插件
- 🚀 **高性能** - 协程/线程/进程池，资源复用
- 🎼 **工作流编排** - DAG 工作流引擎
- 🔧 **配置管理** - 统一配置中心，支持热更新
- 🛠️ **治理能力** - 限流、熔断、降级、超时控制
- 🐳 **容器化部署** - Docker/Kubernetes 支持

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 或 poetry

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/plugin-execution-system.git
cd plugin-execution-system

# 安装依赖（推荐使用虚拟环境）
cd v2
pip install -r requirements.txt
```

### 运行示例

```bash
# 运行主程序
python main.py

# 使用 Docker
docker-compose up -d
```

### 基础使用

```python
from core.base import PluginBase, PluginMetadata, PluginType

class MyPlugin(PluginBase):
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="my_plugin",
            version="1.0.0",
            type=PluginType.PROCESSOR,
            description="My custom plugin"
        )

    def run(self, data: dict) -> dict:
        return {"result": "processed"}
```

## 📁 项目结构

```
plugin-execution-system/
├── v2/                          # v2.0 主版本（当前版本）
│   ├── core/                    # 核心框架
│   │   ├── management/          # 插件管理层
│   │   ├── execution/           # 插件执行层
│   │   ├── orchestration/       # 编排层
│   │   ├── observability/       # 可观测层
│   │   └── adapters/            # 多语言适配器
│   ├── plugins/                 # 插件目录
│   │   ├── builtin/             # 内置插件
│   │   └── external/            # 外部插件
│   ├── api/                     # API 网关
│   ├── config/                  # 配置文件
│   ├── tests/                   # 测试
│   ├── examples/                # 示例代码
│   ├── docs/                    # 详细文档
│   └── README.md                # v2 版本说明
│
├── docs/                        # 项目文档
│   ├── design/                  # 设计文档
│   │   ├── v1-design.md         # v1 设计方案
│   │   └── v2-design.md         # v2 设计方案
│   ├── architecture.md          # 架构设计
│   ├── plugin-development.md   # 插件开发指南
│   ├── api-reference.md        # API 参考
│   └── deployment.md           # 部署指南
│
├── CHANGELOG.md                 # 版本变更日志
├── CONTRIBUTING.md              # 贡献指南
├── LICENSE                      # 许可证
└── README.md                    # 项目主文档（本文件）
```

## 📌 版本说明

### 当前版本：v2.0.0

v2.0 是企业级重构版本，在 v1 基础上进行了全面升级。

| 版本 | 状态 | 说明 | 文档 |
|------|------|------|------|
| **v2.0** | ✅ 当前版本 | 企业级插件系统，支持高并发、可观测、多语言 | [v2 README](v2/README.md) |
| v1.0 | 📚 已归档 | 基础插件系统，核心功能验证 | [v1 设计文档](docs/design/v1-design.md) |

### 版本对比

| 特性 | v1.0 | v2.0 |
|------|------|------|
| 插件接口规范 | ✅ | ✅ |
| 动态加载 | ✅ | ✅ |
| 异常隔离 | ✅ | ✅ |
| 并发执行 | ❌ | ✅ |
| 生命周期管理 | 基础 | 完整 |
| 依赖解析 | ❌ | ✅ |
| 工作流编排 | ❌ | ✅ |
| 可观测性 | ❌ | ✅ |
| 多语言支持 | ❌ | ✅ |
| API 网关 | ❌ | ✅ |
| 容器化部署 | ❌ | ✅ |

详细变更请查看 [CHANGELOG.md](CHANGELOG.md)

## 📖 文档

### 核心文档

- [架构设计](docs/architecture.md) - 系统架构与设计理念
- [插件开发指南](docs/plugin-development.md) - 如何开发自定义插件
- [API 参考](docs/api-reference.md) - HTTP/gRPC API 文档
- [部署指南](docs/deployment.md) - 生产环境部署方案

### 设计文档

- [v1 设计方案](docs/design/v1-design.md) - v1 版本设计思路
- [v2 设计方案](docs/design/v2-design.md) - v2 版本架构设计

### 快速链接

- [快速开始](v2/docs/quickstart.md)
- [示例代码](v2/examples/)
- [常见问题](docs/FAQ.md)

## 🛠️ 开发指南

### 开发环境设置

```bash
# 安装开发依赖
pip install -r v2/requirements.txt

# 运行测试
cd v2
pytest tests/

# 代码格式化
black .

# 代码检查
flake8 .
mypy .
```

### 创建新插件

1. 在 `v2/plugins/builtin/` 或 `v2/plugins/external/` 创建插件文件
2. 继承 `PluginBase` 并实现必要方法
3. 系统会自动发现并加载插件

详细说明请参考 [插件开发指南](docs/plugin-development.md)

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_plugin_loader.py

# 生成覆盖率报告
pytest --cov=core --cov-report=html
```

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

详细贡献指南请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

感谢所有贡献者对本项目的支持！

## 📮 联系方式

- 提交 Issue: [GitHub Issues](https://github.com/qiuqiumaoearth/plugin-execution-system/issues)
- 邮件: qiuqiuqiumao@qq.com

---

⭐ 如果这个项目对你有帮助，请给个 Star！
