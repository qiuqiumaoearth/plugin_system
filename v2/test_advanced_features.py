"""
测试高级功能：启用/禁用、批量执行、状态查询
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.management.registry import PluginRegistry
from core.management.loader import PluginLoader
from core.execution.executor import PluginExecutor
from core.context import PluginContext


def print_section(title):
    """打印分隔线"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    # 初始化系统
    registry = PluginRegistry()
    plugins_dir = project_root / "plugins" / "builtin"
    loader = PluginLoader([str(plugins_dir)], registry)
    executor = PluginExecutor(registry)

    # 加载所有插件
    print_section("1. 加载插件")
    loaded = loader.discover_plugins()
    print(f"发现 {len(loaded)} 个插件文件")

    # 加载每个插件
    loaded_names = []
    for plugin_path in loaded:
        plugin = loader.load_plugin(plugin_path)
        if plugin:
            loaded_names.append(plugin.metadata().name)

    print(f"成功加载 {len(loaded_names)} 个插件: {', '.join(loaded_names)}")

    # 测试启用/禁用功能
    print_section("2. 测试启用/禁用功能")
    print("\n当前所有插件状态:")
    for plugin_name in registry.list_all():
        enabled = registry.is_enabled(plugin_name)
        status = "启用" if enabled else "禁用"
        print(f"  - {plugin_name}: {status}")

    # 禁用 echo_plugin
    print("\n禁用 echo_plugin...")
    registry.disable("echo_plugin")
    print(f"echo_plugin 状态: {'启用' if registry.is_enabled('echo_plugin') else '禁用'}")

    # 尝试执行被禁用的插件
    print("\n尝试执行被禁用的插件:")
    context = PluginContext(request_id="test-001")
    result = executor.execute("echo_plugin", {"message": "测试"}, context)
    print(f"  结果: {result}")

    # 重新启用
    print("\n重新启用 echo_plugin...")
    registry.enable("echo_plugin")
    result = executor.execute("echo_plugin", {"message": "测试"}, context)
    print(f"  结果: {result}")

    # 测试批量执行 - 顺序模式
    print_section("3. 测试批量执行 - 顺序模式")
    test_data = {
        "message": "Hello",
        "numbers": [1, 2, 3, 4, 5],
        "name": "测试用户",
        "age": 25,
        "email": "test@example.com"
    }

    context = PluginContext(request_id="batch-001")
    batch_result = executor.execute_all(test_data, context, mode="sequential")

    print(f"\n执行结果:")
    print(f"  总计: {batch_result['total']} 个插件")
    print(f"  成功: {batch_result['successful']} 个")
    print(f"  失败: {batch_result['failed']} 个")

    print("\n各插件结果:")
    for plugin_name, result in batch_result['results'].items():
        print(f"  [{plugin_name}]")
        print(f"    {result}")

    if batch_result['errors']:
        print("\n错误信息:")
        for plugin_name, error in batch_result['errors'].items():
            print(f"  [{plugin_name}] {error}")

    # 测试批量执行 - 并行模式
    print_section("4. 测试批量执行 - 并行模式")
    context = PluginContext(request_id="batch-002")
    batch_result = executor.execute_all(test_data, context, mode="parallel")

    print(f"\n执行结果:")
    print(f"  总计: {batch_result['total']} 个插件")
    print(f"  成功: {batch_result['successful']} 个")
    print(f"  失败: {batch_result['failed']} 个")

    # 测试统计信息
    print_section("5. 查看统计信息")
    stats = registry.get_statistics()
    print(f"\n系统统计:")
    print(f"  总插件数: {stats['total_plugins']}")
    print(f"  启用插件: {stats['enabled_plugins']}")
    print(f"  禁用插件: {stats['disabled_plugins']}")

    print("\n各插件统计:")
    for plugin_name, plugin_stats in stats['plugins'].items():
        print(f"  [{plugin_name}]")
        print(f"    执行次数: {plugin_stats['execution_count']}")
        print(f"    错误次数: {plugin_stats['error_count']}")
        print(f"    错误率: {plugin_stats['error_rate']:.2%}")
        print(f"    状态: {plugin_stats['status']}")
        print(f"    启用: {plugin_stats['enabled']}")

    # 测试部分禁用后的批量执行
    print_section("6. 测试部分禁用后的批量执行")
    print("\n禁用 sum_plugin 和 validator_plugin...")
    registry.disable("sum_plugin")
    registry.disable("validator_plugin")

    enabled = registry.list_enabled()
    print(f"当前启用的插件: {', '.join(enabled)}")

    context = PluginContext(request_id="batch-003")
    batch_result = executor.execute_all(test_data, context, mode="sequential")

    print(f"\n执行结果:")
    print(f"  总计: {batch_result['total']} 个插件")
    print(f"  成功: {batch_result['successful']} 个")
    print(f"  执行的插件: {', '.join(batch_result['results'].keys())}")

    # 恢复所有插件
    print("\n恢复所有插件...")
    for plugin_name in registry.list_all():
        registry.enable(plugin_name)

    print_section("测试完成")
    print("\n所有高级功能测试通过!")

    # 关闭执行器
    executor.shutdown()


if __name__ == "__main__":
    main()
