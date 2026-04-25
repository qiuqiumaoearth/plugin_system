"""
插件执行器 - 统一执行入口
"""

from typing import Dict, Any
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

from core.management.registry import PluginRegistry
from core.context import PluginContext


class PluginExecutor:
    """插件执行器"""

    def __init__(self, registry: PluginRegistry, thread_pool_size: int = 10):
        self.registry = registry
        self.thread_pool = ThreadPoolExecutor(max_workers=thread_pool_size)

    def execute(self,
                plugin_name: str,
                data: Dict[str, Any],
                context: PluginContext) -> Dict[str, Any]:
        """执行插件（同步）"""
        # 1. 获取插件
        plugin = self.registry.get(plugin_name)
        if not plugin:
            return self._error_response(plugin_name, "Plugin not found")

        # 2. 检查插件是否启用
        if not self.registry.is_enabled(plugin_name):
            return self._error_response(plugin_name, "Plugin is disabled")

        # 3. 设置上下文
        plugin.set_context(context)

        # 4. 执行插件
        try:
            context.log("info", f"Executing plugin: {plugin_name}")
            start_time = time.time()

            # 执行
            result = plugin.run(data)

            # 记录指标
            execution_time = time.time() - start_time
            context.record_metric(
                "plugin_execution_time",
                execution_time,
                {"plugin": plugin_name}
            )

            # 记录成功
            self.registry.record_execution(plugin_name, True)

            return self._success_response(plugin_name, result)

        except Exception as e:
            context.log("error", f"Plugin execution failed: {str(e)}")
            plugin.on_error(e)
            self.registry.record_execution(plugin_name, False, e)
            return self._error_response(plugin_name, str(e))

    async def execute_async(self,
                           plugin_name: str,
                           data: Dict[str, Any],
                           context: PluginContext) -> Dict[str, Any]:
        """执行插件（异步）"""
        plugin = self.registry.get(plugin_name)
        if not plugin:
            return self._error_response(plugin_name, "Plugin not found")

        if not self.registry.is_enabled(plugin_name):
            return self._error_response(plugin_name, "Plugin is disabled")

        plugin.set_context(context)

        try:
            context.log("info", f"Executing plugin async: {plugin_name}")
            start_time = time.time()

            # 异步执行
            result = await plugin.run_async(data)

            execution_time = time.time() - start_time
            context.record_metric(
                "plugin_execution_time",
                execution_time,
                {"plugin": plugin_name, "mode": "async"}
            )

            self.registry.record_execution(plugin_name, True)
            return self._success_response(plugin_name, result)

        except Exception as e:
            context.log("error", f"Plugin async execution failed: {str(e)}")
            plugin.on_error(e)
            self.registry.record_execution(plugin_name, False, e)
            return self._error_response(plugin_name, str(e))

    def execute_with_timeout(self,
                            plugin_name: str,
                            data: Dict[str, Any],
                            context: PluginContext,
                            timeout: int) -> Dict[str, Any]:
        """带超时的执行"""
        future = self.thread_pool.submit(
            self.execute, plugin_name, data, context
        )

        try:
            return future.result(timeout=timeout)
        except FuturesTimeoutError:
            future.cancel()
            return self._error_response(
                plugin_name,
                f"Execution timeout after {timeout} seconds"
            )

    def _success_response(self, plugin_name: str, result: Any) -> Dict[str, Any]:
        """成功响应"""
        return {
            "success": True,
            "plugin": plugin_name,
            "result": result,
            "error": None
        }

    def _error_response(self, plugin_name: str, error: str) -> Dict[str, Any]:
        """错误响应"""
        return {
            "success": False,
            "plugin": plugin_name,
            "result": None,
            "error": error
        }

    def shutdown(self):
        """关闭执行器"""
        self.thread_pool.shutdown(wait=True)
