"""
Echo 插件 - 回显输入内容
"""

from core.base import PluginBase, PluginMetadata, PluginType
from typing import Dict, Any


class EchoPlugin(PluginBase):
    """Echo 插件"""

    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="echo_plugin",
            version="1.0.0",
            type=PluginType.PROCESSOR,
            description="Echo plugin that returns the input data",
            author="Plugin System Team",
            license="MIT",
            timeout_seconds=10,
            supports_async=True,
            tags=["example", "basic"]
        )

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """回显输入数据"""
        prefix = self.get_config("prefix", "[ECHO]")

        return {
            "echo": f"{prefix} {data}",
            "original": data
        }
