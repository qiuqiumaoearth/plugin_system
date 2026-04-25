# -*- coding: utf-8 -*-
"""
测试新创建的问候插件
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.management.registry import PluginRegistry
from core.management.loader import PluginLoader
from core.execution.executor import PluginExecutor
from core.context import PluginContext


print("=" * 60)
print("测试新插件：问候插件")
print("=" * 60)

# 准备插件系统
print("\n[1] 启动插件系统...")
registry = PluginRegistry()
loader = PluginLoader(["plugins/builtin"], registry)
executor = PluginExecutor(registry)
context = PluginContext()

# 加载所有插件
print("[2] 加载插件...")
plugins = loader.discover_plugins()
for plugin_path in plugins:
    loader.load_plugin(plugin_path)

# 列出所有插件
all_plugins = registry.list_all()
print(f"[3] 成功加载 {len(all_plugins)} 个插件:")
for name in all_plugins:
    print(f"    - {name}")

# 测试问候插件
print("\n" + "=" * 60)
print("测试问候插件")
print("=" * 60)

# 测试 1: 问候张三
print("\n[测试 1] 问候张三")
result = executor.execute(
    plugin_name="greeting_plugin",
    data={"name": "张三"},
    context=context
)

if result["success"]:
    print(f"问候语: {result['result']['greeting']}")
    print(f"时间段: {result['result']['time_period']}")
    print(f"当前小时: {result['result']['hour']}")
else:
    print(f"出错了: {result['error']}")

# 测试 2: 问候李四
print("\n[测试 2] 问候李四")
result = executor.execute(
    plugin_name="greeting_plugin",
    data={"name": "李四"},
    context=context
)

if result["success"]:
    print(f"问候语: {result['result']['greeting']}")
else:
    print(f"出错了: {result['error']}")

# 测试 3: 不提供名字（使用默认）
print("\n[测试 3] 不提供名字")
result = executor.execute(
    plugin_name="greeting_plugin",
    data={},
    context=context
)

if result["success"]:
    print(f"问候语: {result['result']['greeting']}")
else:
    print(f"出错了: {result['error']}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
print("""
你刚才看到了如何创建和使用新插件：

1. 创建插件文件（greeting_plugin.py）
2. 继承 PluginBase 类
3. 实现 metadata() 和 run() 方法
4. 系统自动发现并加载插件
5. 通过 executor.execute() 调用插件

就这么简单！
""")
