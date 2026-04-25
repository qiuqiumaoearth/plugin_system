# Plugin Execution System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

Enterprise-grade plugin execution system with high concurrency, high availability, observability, and extensibility.

[简体中文](README.md) | English

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Version Information](#version-information)
- [Documentation](#documentation)
- [Development Guide](#development-guide)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Capabilities

- 🔌 **Unified Plugin Interface** - Standardized plugin development specification
- 🔄 **Dynamic Loading** - Support for plugin hot loading and unloading
- 🎯 **Lifecycle Management** - Complete plugin lifecycle hooks
- 🔗 **Dependency Resolution** - Automatic handling of plugin dependencies
- ⚡ **Concurrent Execution** - Support for serial/parallel/async execution modes
- 🛡️ **Exception Isolation** - Plugin failures don't affect system stability

### Enterprise Features

- 📊 **Observability** - Structured logging, metrics collection, distributed tracing
- 🔐 **Security Isolation** - Process-level isolation, resource quotas, permission management
- 🌐 **Multi-language Support** - Python/Go/JavaScript/Rust plugins
- 🚀 **High Performance** - Coroutines/threads/process pools, resource reuse
- 🎼 **Workflow Orchestration** - DAG workflow engine
- 🔧 **Configuration Management** - Unified configuration center with hot reload
- 🛠️ **Governance** - Rate limiting, circuit breaking, degradation, timeout control
- 🐳 **Container Deployment** - Docker/Kubernetes support

## 🚀 Quick Start

### Requirements

- Python 3.8+
- pip or poetry

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/plugin-execution-system.git
cd plugin-execution-system

# Install dependencies (virtual environment recommended)
cd v2
pip install -r requirements.txt
```

### Run Example

```bash
# Run main program
python main.py

# Using Docker
docker-compose up -d
```

### Basic Usage

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

## 📁 Project Structure

```
plugin-execution-system/
├── v2/                          # v2.0 main version (current)
│   ├── core/                    # Core framework
│   │   ├── management/          # Plugin management layer
│   │   ├── execution/           # Plugin execution layer
│   │   ├── orchestration/       # Orchestration layer
│   │   ├── observability/       # Observability layer
│   │   └── adapters/            # Multi-language adapters
│   ├── plugins/                 # Plugin directory
│   │   ├── builtin/             # Built-in plugins
│   │   └── external/            # External plugins
│   ├── api/                     # API gateway
│   ├── config/                  # Configuration files
│   ├── tests/                   # Tests
│   ├── examples/                # Example code
│   ├── docs/                    # Detailed documentation
│   └── README.md                # v2 version documentation
│
├── docs/                        # Project documentation
│   ├── design/                  # Design documents
│   │   ├── v1-design.md         # v1 design proposal
│   │   └── v2-design.md         # v2 design proposal
│   ├── architecture.md          # Architecture design
│   ├── plugin-development.md   # Plugin development guide
│   ├── api-reference.md        # API reference
│   └── deployment.md           # Deployment guide
│
├── CHANGELOG.md                 # Version changelog
├── CONTRIBUTING.md              # Contributing guide
├── LICENSE                      # License
└── README.md                    # Main project documentation
```

## 📌 Version Information

### Current Version: v2.0.0

v2.0 is an enterprise-grade refactored version with comprehensive upgrades from v1.

| Version | Status | Description | Documentation |
|---------|--------|-------------|---------------|
| **v2.0** | ✅ Current | Enterprise plugin system with high concurrency, observability, multi-language | [v2 README](v2/README.md) |
| v1.0 | 📚 Archived | Basic plugin system, core functionality validation | [v1 Design Doc](docs/design/v1-design.md) |

### Version Comparison

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Plugin Interface | ✅ | ✅ |
| Dynamic Loading | ✅ | ✅ |
| Exception Isolation | ✅ | ✅ |
| Concurrent Execution | ❌ | ✅ |
| Lifecycle Management | Basic | Complete |
| Dependency Resolution | ❌ | ✅ |
| Workflow Orchestration | ❌ | ✅ |
| Observability | ❌ | ✅ |
| Multi-language Support | ❌ | ✅ |
| API Gateway | ❌ | ✅ |
| Container Deployment | ❌ | ✅ |

See [CHANGELOG.md](CHANGELOG.md) for detailed changes

## 📖 Documentation

### Core Documentation

- [Architecture Design](docs/architecture.md) - System architecture and design philosophy
- [Plugin Development Guide](docs/plugin-development.md) - How to develop custom plugins
- [API Reference](docs/api-reference.md) - HTTP/gRPC API documentation
- [Deployment Guide](docs/deployment.md) - Production deployment solutions

### Design Documents

- [v1 Design Proposal](docs/design/v1-design.md) - v1 version design approach
- [v2 Design Proposal](docs/design/v2-design.md) - v2 version architecture design

### Quick Links

- [Quick Start](v2/docs/quickstart.md)
- [Example Code](v2/examples/)
- [FAQ](docs/FAQ.md)

## 🛠️ Development Guide

### Development Environment Setup

```bash
# Install development dependencies
pip install -r v2/requirements.txt

# Run tests
cd v2
pytest tests/

# Code formatting
black .

# Code linting
flake8 .
mypy .
```

### Creating New Plugins

1. Create plugin file in `v2/plugins/builtin/` or `v2/plugins/external/`
2. Inherit from `PluginBase` and implement required methods
3. System will automatically discover and load the plugin

See [Plugin Development Guide](docs/plugin-development.md) for details

### Running Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_plugin_loader.py

# Generate coverage report
pytest --cov=core --cov-report=html
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

Thanks to all contributors for their support!

## 📮 Contact

- Submit Issue: [GitHub Issues](https://github.com/yourusername/plugin-execution-system/issues)
- Email: qiuqiuqiumao@qq.com

---

⭐ Star this project if it helps you!
