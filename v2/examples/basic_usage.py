"""
基础使用示例
"""

from core.management.registry import PluginRegistry
from core.management.lifecycle import LifecycleManager
from core.management.loader import PluginLoader
from core.execution.executor import PluginExecutor
from core.execution.scheduler import PluginScheduler
from core.context import PluginContext
from core.observability.logger import StructuredLogger


def main():
    """基础使用示例"""
    print("=== Plugin System v2 - Basic Usage Example ===\n")

    # 1. 创建核心组件
    registry = PluginRegistry()
    lifecycle = LifecycleManager(registry)
    loader = PluginLoader(["plugins/builtin"], registry)
    executor = PluginExecutor(registry)
    scheduler = PluginScheduler(executor)
    logger = StructuredLogger("Example")

    # 2. 加载插件
    print("Loading plugins...")
    plugins = loader.discover_plugins()
    for plugin_path in plugins:
        plugin = loader.load_plugin(plugin_path)
        if plugin:
            print(f"  ✓ Loaded: {plugin.metadata().name} v{plugin.metadata().version}")

    # 3. 初始化插件
    print("\nInitializing plugins...")
    for plugin_name in registry.list_all():
        lifecycle.initialize_plugin(plugin_name, {})
        print(f"  ✓ Initialized: {plugin_name}")

    # 4. 执行单个插件
    print("\n--- Example 1: Execute Single Plugin ---")
    context = PluginContext(logger=logger)
    result = executor.execute("echo_plugin", {"message": "Hello World"}, context)
    print(f"Result: {result}")

    # 5. 执行 sum 插件
    print("\n--- Example 2: Execute Sum Plugin ---")
    result = executor.execute("sum_plugin", {"numbers": [1, 2, 3, 4, 5]}, context)
    print(f"Result: {result}")

    # 6. 串行执行多个插件
    print("\n--- Example 3: Serial Execution ---")
    results = scheduler.execute_serial(
        ["echo_plugin", "sum_plugin"],
        {"message": "test", "numbers": [10, 20, 30]},
        context
    )
    for i, result in enumerate(results):
        print(f"Step {i+1}: {result}")

    # 7. 并行执行多个插件
    print("\n--- Example 4: Parallel Execution ---")
    results = scheduler.execute_parallel(
        ["echo_plugin", "sum_plugin"],
        {"message": "parallel", "numbers": [1, 2, 3]},
        context
    )
    for i, result in enumerate(results):
        print(f"Plugin {i+1}: {result}")

    # 8. 查看统计信息
    print("\n--- Statistics ---")
    stats = registry.get_statistics()
    print(f"Total plugins: {stats['total_plugins']}")
    print(f"Enabled plugins: {stats['enabled_plugins']}")
    for name, info in stats['plugins'].items():
        print(f"  {name}: {info['execution_count']} executions, {info['error_count']} errors")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
