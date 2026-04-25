"""
插件调度器 - 支持串行、并行、DAG 执行
"""

from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import asyncio

from core.execution.executor import PluginExecutor
from core.context import PluginContext


class PluginScheduler:
    """插件调度器"""

    def __init__(self, executor: PluginExecutor):
        self.executor = executor

    def execute_serial(self,
                      plugin_names: List[str],
                      data: Dict[str, Any],
                      context: PluginContext) -> List[Dict[str, Any]]:
        """串行执行多个插件"""
        results = []
        current_data = data

        for plugin_name in plugin_names:
            result = self.executor.execute(plugin_name, current_data, context)
            results.append(result)

            # 如果失败，停止执行
            if not result["success"]:
                break

            # 将结果作为下一个插件的输入
            current_data = result["result"]

        return results

    def execute_parallel(self,
                        plugin_names: List[str],
                        data: Dict[str, Any],
                        context: PluginContext) -> List[Dict[str, Any]]:
        """并行执行多个插件"""
        with ThreadPoolExecutor(max_workers=len(plugin_names)) as pool:
            futures = [
                pool.submit(self.executor.execute, name, data, context)
                for name in plugin_names
            ]

            results = [future.result() for future in futures]

        return results

    async def execute_parallel_async(self,
                                    plugin_names: List[str],
                                    data: Dict[str, Any],
                                    context: PluginContext) -> List[Dict[str, Any]]:
        """异步并行执行"""
        tasks = [
            self.executor.execute_async(name, data, context)
            for name in plugin_names
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理异常
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(
                    self.executor._error_response(
                        plugin_names[i],
                        str(result)
                    )
                )
            else:
                processed_results.append(result)

        return processed_results

    def execute_with_dependencies(self,
                                  execution_plan: List[List[str]],
                                  data: Dict[str, Any],
                                  context: PluginContext) -> Dict[str, Any]:
        """按依赖顺序执行插件（DAG）

        execution_plan: 二维列表，每个子列表是一个执行阶段，阶段内的插件可以并行执行
        例如: [['plugin_a'], ['plugin_b', 'plugin_c'], ['plugin_d']]
        """
        all_results = {}
        current_data = data

        for stage in execution_plan:
            # 并行执行当前阶段的所有插件
            stage_results = self.execute_parallel(stage, current_data, context)

            # 收集结果
            for plugin_name, result in zip(stage, stage_results):
                all_results[plugin_name] = result

                # 如果有插件失败，停止执行
                if not result["success"]:
                    return {
                        "success": False,
                        "results": all_results,
                        "error": f"Plugin {plugin_name} failed"
                    }

            # 合并结果作为下一阶段的输入
            if stage_results:
                # 简单策略：使用最后一个成功的结果
                for result in reversed(stage_results):
                    if result["success"]:
                        current_data = result["result"]
                        break

        return {
            "success": True,
            "results": all_results,
            "error": None
        }
