#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本 - 演示如何使用插件系统
这个脚本不需要启动完整的服务器，直接测试插件功能
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from core.management.registry import PluginRegistry
from core.management.loader import PluginLoader
from core.execution.executor import PluginExecutor
from core.context import PluginContext


def print_separator(title=""):
    """打印分隔线"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"{'='*60}\n")


def main():
    print_separator("插件系统简单测试")

    # 1. 创建插件注册表
    print("[步骤 1] 创建插件注册表...")
    registry = PluginRegistry()
    print("[成功] 插件注册表创建成功\n")

    # 2. 创建插件加载器
    print("[步骤 2] 创建插件加载器...")
    plugin_dirs = ["plugins/builtin"]  # 指定插件目录
    loader = PluginLoader(plugin_dirs, registry)
    print("[成功] 插件加载器创建成功\n")

    # 3. 发现并加载插件
    print("[步骤 3] 发现并加载插件...")
    plugins = loader.discover_plugins()
    print(f"[发现] 找到 {len(plugins)} 个插件文件:")
    for plugin_path in plugins:
        print(f"   - {plugin_path}")

    print("\n[加载] 开始加载插件...")
    for plugin_path in plugins:
        plugin = loader.load_plugin(plugin_path)
        if plugin:
            metadata = plugin.metadata()
            print(f"[成功] 加载成功: {metadata.name} v{metadata.version}")
            print(f"   描述: {metadata.description}")

    # 4. 列出所有已加载的插件
    print_separator("已加载的插件列表")
    all_plugins = registry.list_all()
    print(f"共有 {len(all_plugins)} 个插件已加载:\n")

    for plugin_name in all_plugins:
        plugin_info = registry.get_info(plugin_name)
        if plugin_info:
            metadata = plugin_info['metadata']
            print(f"[插件] {plugin_name}")
            print(f"   版本: {metadata.version}")
            print(f"   状态: {plugin_info['status']}")
            print(f"   类型: {metadata.type}")
            print(f"   启用: {plugin_info['enabled']}")
            print()

    # 5. 创建执行器和上下文
    print_separator("测试插件执行")
    executor = PluginExecutor(registry)
    context = PluginContext()

    # 6. 测试 echo_plugin
    print("[测试 1] Echo Plugin")
    print("输入数据: {'message': 'Hello, Plugin System!'}")

    result = executor.execute(
        plugin_name="echo_plugin",
        data={"message": "Hello, Plugin System!"},
        context=context
    )

    if result["success"]:
        print("[成功] 执行成功!")
        print(f"返回结果: {result['result']}")
    else:
        print(f"[失败] 执行失败: {result['error']}")

    # 7. 测试 sum_plugin
    print("\n[测试 2] Sum Plugin")
    print("输入数据: {'numbers': [1, 2, 3, 4, 5]}")

    result = executor.execute(
        plugin_name="sum_plugin",
        data={"numbers": [1, 2, 3, 4, 5]},
        context=context
    )

    if result["success"]:
        print("[成功] 执行成功!")
        print(f"返回结果: {result['result']}")
        print(f"   总和: {result['result']['sum']}")
        print(f"   数量: {result['result']['count']}")
        print(f"   平均值: {result['result']['average']}")
    else:
        print(f"[失败] 执行失败: {result['error']}")

    # 8. 测试错误处理
    print("\n[测试 3] 错误处理（传入错误数据）")
    print("输入数据: {'numbers': 'not a list'}")

    result = executor.execute(
        plugin_name="sum_plugin",
        data={"numbers": "not a list"},
        context=context
    )

    if result["success"]:
        print("[成功] 执行成功!")
        print(f"返回结果: {result['result']}")
    else:
        print("[失败] 执行失败（这是预期的）")
        print(f"错误信息: {result['error']}")

    # 9. 测试不存在的插件
    print("\n[测试 4] 调用不存在的插件")
    print("插件名称: 'nonexistent_plugin'")

    result = executor.execute(
        plugin_name="nonexistent_plugin",
        data={"test": "data"},
        context=context
    )

    if result["success"]:
        print("[成功] 执行成功!")
        print(f"返回结果: {result['result']}")
    else:
        print("[失败] 执行失败（这是预期的）")
        print(f"错误信息: {result['error']}")

    print_separator("测试完成")
    print("[完成] 所有测试已完成！")
    print("\n[提示]")
    print("   - 插件系统可以动态加载插件")
    print("   - 插件执行有异常隔离，单个插件失败不影响系统")
    print("   - 可以在 plugins/builtin/ 目录添加更多插件")
    print("   - 运行 'python main.py' 启动完整的 HTTP API 服务器")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[错误] 发生错误: {e}")
        import traceback
        traceback.print_exc()
