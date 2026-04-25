# -*- coding: utf-8 -*-
"""
超级简单的插件使用示例
适合完全不懂编程的小白
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.management.registry import PluginRegistry
from core.management.loader import PluginLoader
from core.execution.executor import PluginExecutor
from core.context import PluginContext


print("=" * 60)
print("欢迎使用插件系统！")
print("=" * 60)

# 第 1 步：准备插件系统
print("\n[准备] 正在启动插件系统...")
registry = PluginRegistry()
loader = PluginLoader(["plugins/builtin"], registry)
executor = PluginExecutor(registry)
context = PluginContext()

# 第 2 步：加载插件
print("[加载] 正在加载插件...")
plugins = loader.discover_plugins()
for plugin_path in plugins:
    loader.load_plugin(plugin_path)
print(f"[完成] 成功加载 {len(registry.list_all())} 个插件\n")

# ============================================================
# 示例 1: 使用 Echo 插件（回声）
# ============================================================
print("=" * 60)
print("示例 1: Echo 插件 - 回声功能")
print("=" * 60)

print("\n我要说: 'Hello, World!'")
result = executor.execute(
    plugin_name="echo_plugin",
    data={"message": "Hello, World!"},
    context=context
)

if result["success"]:
    print(f"插件回复: {result['result']['echo']}")
else:
    print(f"出错了: {result['error']}")

# ============================================================
# 示例 2: 使用 Sum 插件（计算器）
# ============================================================
print("\n" + "=" * 60)
print("示例 2: Sum 插件 - 计算器功能")
print("=" * 60)

numbers = [10, 20, 30, 40, 50]
print(f"\n我要计算这些数字的和: {numbers}")

result = executor.execute(
    plugin_name="sum_plugin",
    data={"numbers": numbers},
    context=context
)

if result["success"]:
    print(f"总和: {result['result']['sum']}")
    print(f"数量: {result['result']['count']}")
    print(f"平均值: {result['result']['average']}")
else:
    print(f"出错了: {result['error']}")

# ============================================================
# 示例 3: 使用 Validator 插件（数据检查）
# ============================================================
print("\n" + "=" * 60)
print("示例 3: Validator 插件 - 数据验证功能")
print("=" * 60)

# 测试 1: 正确的数据
print("\n[测试 1] 检查正确的数据:")
good_data = {
    "name": "张三",
    "age": 25,
    "email": "zhangsan@example.com"
}
print(f"数据: {good_data}")

result = executor.execute(
    plugin_name="validator_plugin",
    data=good_data,
    context=context
)

if result["success"]:
    if result['result']['valid']:
        print("[结果] 数据有效！")
    else:
        print(f"[结果] 数据无效: {result['result']['errors']}")

# 测试 2: 错误的数据
print("\n[测试 2] 检查错误的数据:")
bad_data = {
    "name": "李四",
    "age": "不是数字",  # 错误：年龄应该是数字
    "email": "notanemail"  # 错误：邮箱格式不对
}
print(f"数据: {bad_data}")

result = executor.execute(
    plugin_name="validator_plugin",
    data=bad_data,
    context=context
)

if result["success"]:
    if result['result']['valid']:
        print("[结果] 数据有效！")
    else:
        print("[结果] 数据无效，发现以下错误:")
        for error in result['result']['errors']:
            print(f"  - {error}")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("总结")
print("=" * 60)
print("""
你刚才看到了 3 个插件的功能：

1. Echo 插件 - 回声功能
   输入什么，就返回什么（加个前缀）

2. Sum 插件 - 计算器功能
   输入一组数字，计算总和、数量、平均值

3. Validator 插件 - 数据验证功能
   检查数据是否符合要求（年龄是数字、邮箱有@符号）

这就是插件系统的核心思想：
- 主程序负责管理
- 插件负责具体功能
- 你可以随时添加新插件，不需要改主程序
""")

print("\n想创建自己的插件？查看 USER_GUIDE.md 文档！")
print("=" * 60)
