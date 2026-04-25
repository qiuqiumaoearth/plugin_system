# 插件化执行系统 v2.0

企业级插件化执行系统，支持高并发、高可用、可观测、可扩展。

## 特性

- ✅ 统一插件接口规范
- ✅ 插件动态加载与热更新
- ✅ 插件生命周期管理
- ✅ 插件依赖解析
- ✅ 并发执行（串行/并行/异步）
- ✅ 超时控制与熔断保护
- ✅ 工作流编排引擎
- ✅ 结构化日志与指标采集
- ✅ 多语言插件支持
- ✅ HTTP/gRPC API 接口
- ✅ Docker/K8s 部署支持

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行系统

```bash
python main.py
```

### 使用 Docker

```bash
docker-compose up -d
```

## 项目结构

```
plugin_system_v2/
├── config/                 # 配置文件
├── core/                   # 核心框架
│   ├── management/         # 插件管理层
│   ├── execution/          # 插件执行层
│   ├── orchestration/      # 编排层
│   ├── observability/      # 可观测层
│   └── adapters/           # 多语言适配器
├── plugins/                # 插件目录
│   ├── builtin/            # 内置插件
│   └── external/           # 外部插件
├── api/                    # API 网关
├── storage/                # 存储层
├── tests/                  # 测试
├── examples/               # 示例
└── docs/                   # 文档
```

## 插件开发

### 创建插件

```python
from core.base import PluginBase, PluginMetadata, PluginType

class MyPlugin(PluginBase):
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="my_plugin",
            version="1.0.0",
            type=PluginType.PROCESSOR,
            description="My custom plugin",
            author="Your Name",
            license="MIT"
        )

    def run(self, data: dict) -> dict:
        # 处理逻辑
        result = {"processed": data}
        return result
```

### 注册插件

将插件文件放入 `plugins/builtin/` 或 `plugins/external/` 目录，系统会自动发现并加载。

## API 使用

### 执行插件

```bash
curl -X POST http://localhost:8080/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "plugin": "echo_plugin",
    "data": {"message": "Hello World"}
  }'
```

### 查看插件列表

```bash
curl http://localhost:8080/api/v1/plugins
```

### 执行工作流

```bash
curl -X POST http://localhost:8080/api/v1/workflow/execute \
  -H "Content-Type: application/json" \
  -d '{
    "workflow": "data_processing",
    "input": {"data": "..."}
  }'
```

## 监控

- Prometheus 指标: http://localhost:9090/metrics
- Grafana 仪表板: http://localhost:3000

## 文档

详细文档请参考 [docs/](docs/) 目录：

- [架构设计](docs/architecture.md)
- [插件开发指南](docs/plugin_development.md)
- [API 参考](docs/api_reference.md)
- [部署指南](docs/deployment.md)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
