"""
插件化执行系统 v2 - 核心模块
"""

__version__ = "2.0.0"
__author__ = "Plugin System Team"

from core.base import PluginBase, PluginMetadata, PluginType, PluginStatus
from core.context import PluginContext

__all__ = [
    "PluginBase",
    "PluginMetadata",
    "PluginType",
    "PluginStatus",
    "PluginContext",
]
