# 插件系统使用指南

## 目录
- [快速开始](#快速开始)
- [基础概念](#基础概念)
- [运行测试](#运行测试)
- [创建自己的插件](#创建自己的插件)
- [启动完整系统](#启动完整系统)
- [常见问题](#常见问题)

---

## 快速开始

### 1. 环境准备

确保你已经安装了 Python 3.8+：

```bash
python --version
```

### 2. 安装依赖

```bash
cd v2
pip install -r requirements.txt
```

### 3. 运行简单测试

```bash
python simple_test.py
```

这个测试脚本会：
- 自动加载所有内置插件
- 测试插件执行功能
- 演示错误处理机制

---

## 基础概念

### 什么是插件系统？

插件系统允许你：
1. **动态加载功能** - 不需要修改主程序，只需添加插件文件
2. **隔离执行** - 单个插件出错不会影响整个系统
3. **灵活扩展** - 可以随时添加新功能

### 核心组件

```
插件系统
├── PluginRegistry (注册表) - 管理所有插件
├── PluginLoader (加载器) - 发现和加载插件
├── PluginExecutor (执行器) - 执行插件
└── PluginContext (上下文) - 提供执行环境
```

### 插件生命周期

```
发现 → 加载 → 初始化 → 执行 → 停止
```

---

## 运行测试

### 方式 1: 简单测试（推荐新手）

```bash
cd v2
python simple_test.py
```

**这个测试会做什么？**
1. 加载 3 个内置插件（echo, sum, validator）
2. 测试 echo 插件 - 回显输入
3. 测试 sum 插件 - 计算数字和
4. 测试错误处理 - 传入错误数据
5. 测试不存在的插件 - 验证错误处理

**预期输出：**
```
[步骤 1] 创建插件注册表...
[成功] 插件注册表创建成功

[步骤 2] 创建插件加载器...
[成功] 插件加载器创建成功

[步骤 3] 发现并加载插件...
[发现] 找到 3 个插件文件
[成功] 加载成功: echo_plugin v1.0.0
[成功] 加载成功: sum_plugin v1.0.0
[成功] 加载成功: validator_plugin v1.0.0

[测试 1] Echo Plugin
[成功] 执行成功!
返回结果: {'echo': "[ECHO] {...}", 'original': {...}}

[测试 2] Sum Plugin
[成功] 执行成功!
返回结果: {'sum': 15, 'count': 5, 'average': 3.0}
```

### 方式 2: 完整系统（启动 HTTP API）

```bash
cd v2
python main.py
```

这会启动一个完整的 HTTP 服务器，可以通过 API 调用插件。

---

## 创建自己的插件

### 步骤 1: 创建插件文件

在 `v2/plugins/builtin/` 目录创建新文件，例如 `my_plugin.py`：

```python
# -*- coding: utf-8 -*-
"""
我的第一个插件
"""

from core.base import PluginBase, PluginMetadata, PluginType
from typing import Dict, Any


class MyPlugin(PluginBase):
    """我的插件"""

    def metadata(self) -> PluginMetadata:
        """插件元数据"""
        return PluginMetadata(
            name="my_plugin",              # 插件名称（唯一）
            version="1.0.0",               # 版本号
            type=PluginType.PROCESSOR,     # 插件类型
            description="我的第一个插件",   # 描述
            author="Your Name",            # 作者
            license="MIT",                 # 许可证
            timeout_seconds=30,            # 超时时间
            tags=["example", "custom"]     # 标签
        )

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        插件执行逻辑
        
        参数:
            data: 输入数据（字典）
            
        返回:
            处理后的数据（字典）
        """
        # 从输入获取数据
        name = data.get("name", "World")
        
        # 处理逻辑
        greeting = f"Hello, {name}!"
        
        # 返回结果
        return {
            "greeting": greeting,
            "length": len(greeting)
        }
```

### 步骤 2: 测试你的插件

创建测试脚本 `test_my_plugin.py`：

```python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.management.registry import PluginRegistry
from core.management.loader import PluginLoader
from core.execution.executor import PluginExecutor
from core.context import PluginContext

# 创建组件
registry = PluginRegistry()
loader = PluginLoader(["plugins/builtin"], registry)
executor = PluginExecutor(registry)
context = PluginContext()

# 加载插件
plugins = loader.discover_plugins()
for plugin_path in plugins:
    loader.load_plugin(plugin_path)

# 测试你的插件
result = executor.execute(
    plugin_name="my_plugin",
    data={"name": "Claude"},
    context=context
)

print(f"成功: {result['success']}")
print(f"结果: {result['result']}")
```

运行测试：

```bash
python test_my_plugin.py
```

### 插件类型说明

```python
PluginType.PROCESSOR     # 数据处理插件
PluginType.FILTER        # 数据过滤插件
PluginType.TRANSFORMER   # 数据转换插件
PluginType.AGGREGATOR    # 数据聚合插件
PluginType.SINK          # 数据输出插件
```

---

## 启动完整系统

### 启动 HTTP API 服务器

```bash
cd v2
python main.py
```

**输出：**
```
[INFO] Starting Plugin System v2...
[INFO] Loading plugins...
[INFO] Discovered 3 plugin(s)
[INFO] Loaded plugin: echo_plugin v1.0.0
[INFO] Loaded plugin: sum_plugin v1.0.0
[INFO] Loaded plugin: validator_plugin v1.0.0
[INFO] Plugin System v2 started successfully
[INFO] API Server: http://localhost:8080
[INFO] Metrics: http://localhost:9090/metrics

Plugin System v2 is running. Press Ctrl+C to stop.
```

### 使用 API 调用插件

**1. 查看所有插件**

```bash
curl http://localhost:8080/api/v1/plugins
```

**2. 执行插件**

```bash
curl -X POST http://localhost:8080/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "plugin": "sum_plugin",
    "data": {"numbers": [1, 2, 3, 4, 5]}
  }'
```

**响应：**
```json
{
  "success": true,
  "plugin": "sum_plugin",
  "result": {
    "sum": 15,
    "count": 5,
    "average": 3.0
  },
  "error": null
}
```

---

## 常见问题

### Q1: 中文显示乱码怎么办？

**原因**: Windows 控制台默认使用 GBK 编码

**解决方案**:
1. 使用 PowerShell 而不是 CMD
2. 或者在 CMD 中运行：`chcp 65001` 切换到 UTF-8

### Q2: 如何查看已加载的插件？

运行 `simple_test.py`，会列出所有已加载的插件。

或者在代码中：

```python
registry = PluginRegistry()
loader = PluginLoader(["plugins/builtin"], registry)
loader.discover_plugins()

# 列出所有插件
all_plugins = registry.list_all()
print(f"已加载 {len(all_plugins)} 个插件:")
for name in all_plugins:
    print(f"  - {name}")
```

### Q3: 插件执行失败怎么办？

插件系统有完善的错误处理：

```python
result = executor.execute(plugin_name="my_plugin", data={...}, context=context)

if result["success"]:
    print(f"成功: {result['result']}")
else:
    print(f"失败: {result['error']}")  # 查看错误信息
```

### Q4: 如何禁用某个插件？

```python
registry.disable("plugin_name")  # 禁用
registry.enable("plugin_name")   # 启用
```

### Q5: 如何添加插件配置？

在插件的 `run()` 方法中：

```python
def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
    # 获取配置（如果没有则使用默认值）
    prefix = self.get_config("prefix", "[DEFAULT]")
    max_items = self.get_config("max_items", 100)
    
    # 使用配置
    result = f"{prefix} {data}"
    return {"result": result}
```

### Q6: 如何调试插件？

在插件代码中添加打印语句：

```python
def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
    print(f"[DEBUG] 输入数据: {data}")
    
    result = process(data)
    
    print(f"[DEBUG] 输出结果: {result}")
    return result
```

---

## 下一步

1. ✅ 运行 `simple_test.py` 熟悉系统
2. ✅ 创建你的第一个插件
3. ✅ 启动完整系统 `python main.py`
4. ✅ 通过 HTTP API 调用插件
5. ✅ 查看项目文档了解更多高级功能

---

## 获取帮助

- 查看示例插件: `v2/plugins/builtin/`
- 查看设计文档: `docs/design/v2-design.md`
- 提交 Issue: https://github.com/qiuqiumaoearth/plugin_system/issues

---

**祝你使用愉快！** 🚀
