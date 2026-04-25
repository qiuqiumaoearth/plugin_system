"""
Sum 插件 - 数字求和
"""

from core.base import PluginBase, PluginMetadata, PluginType
from typing import Dict, Any, List


class SumPlugin(PluginBase):
    """Sum 插件"""

    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="sum_plugin",
            version="1.0.0",
            type=PluginType.PROCESSOR,
            description="Sum plugin that calculates the sum of numbers",
            author="Plugin System Team",
            license="MIT",
            timeout_seconds=30,
            supports_async=True,
            supports_batch=True,
            tags=["math", "calculation"]
        )

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """计算数字列表的和"""
        numbers = data.get("numbers", [])

        # 验证输入
        if not isinstance(numbers, list):
            raise ValueError("'numbers' must be a list")

        if not numbers:
            return {"sum": 0, "count": 0}

        # 验证所有元素都是数字
        for num in numbers:
            if not isinstance(num, (int, float)):
                raise ValueError(f"Invalid number: {num}")

        # 计算和
        total = sum(numbers)

        return {
            "sum": total,
            "count": len(numbers),
            "average": total / len(numbers) if numbers else 0
        }
