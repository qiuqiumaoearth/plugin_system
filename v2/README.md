# 插件化执行系统 v2.0

企业级插件化执行系统，支持高并发、高可用、可观测、可扩展。

## 核心特性

### 基础功能（面试题要求）
- ✅ **插件定义规范**：统一的 PluginBase 基类和 PluginMetadata 元信息
- ✅ **插件加载机制**：动态发现和加载插件，支持热加载
- ✅ **插件管理能力**：注册、注销、启用、禁用、状态查询
- ✅ **异常隔离**：单个插件失败不影响系统和其他插件
- ✅ **元信息获取**：查询插件名称、版本、类型、描述等信息
- ✅ **执行流程**：标准化的插件执行接口和响应格式
- ✅ **启用/禁用**：运行时动态启用或禁用插件

### 高级功能（加分项）
- ✅ **批量执行**：支持顺序执行和并发执行所有插件
- ✅ **超时控制**：防止插件无限执行，可配置超时时间
- ✅ **生命周期管理**：on_load/on_init/on_start/on_stop/on_error 钩子
- ✅ **执行统计**：记录插件执行次数、成功率、平均耗时
- ✅ **线程安全**：注册表使用锁保护，支持并发访问
- ✅ **工作流编排**：支持多插件编排执行（开发中）
- ✅ **多语言支持**：通过适配器支持其他语言插件（规划中）

## 快速开始

### 1. 运行简单示例

```bash
# 最简单的示例 - 了解基本用法
python easy_example.py

# 完整功能演示
python simple_test.py

# 高级功能测试（启用/禁用、批量执行、统计）
python test_advanced_features.py
```

### 2. 创建自己的插件

```python
from core.base import PluginBase, PluginMetadata, PluginType

class MyPlugin(PluginBase):
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="my_plugin",
            version="1.0.0",
            type=PluginType.PROCESSOR,
            description="我的自定义插件",
            author="Your Name"
        )

    def run(self, data: dict) -> dict:
        # 你的处理逻辑
        result = {"processed": data}
        return result
```

将插件文件放入 `plugins/builtin/` 目录，系统会自动发现并加载。

### 3. 使用插件系统

```python
from core.management.registry import PluginRegistry
from core.management.loader import PluginLoader
from core.execution.executor import PluginExecutor
from core.context import PluginContext

# 初始化
registry = PluginRegistry()
loader = PluginLoader(["plugins/builtin"], registry)
executor = PluginExecutor(registry)

# 加载插件
plugins = loader.discover_plugins()
for plugin_path in plugins:
    loader.load_plugin(plugin_path)

# 执行插件
context = PluginContext(request_id="req-001")
result = executor.execute("my_plugin", {"data": "..."}, context)

# 批量执行所有插件
batch_result = executor.execute_all({"data": "..."}, context, mode="parallel")
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

详细文档请参考：

- **[架构设计文档](ARCHITECTURE.md)** - 核心架构、设计决策、数据流
- **[用户使用指南](USER_GUIDE.md)** - 快速上手、插件开发、常见问题
- [设计方案 v2](../../docs/design/v2-design.md) - 完整的设计方案文档

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
