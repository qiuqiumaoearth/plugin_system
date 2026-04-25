"""
插件管理层模块
"""

from core.management.registry import PluginRegistry
from core.management.lifecycle import LifecycleManager
from core.management.config import ConfigManager
from core.management.loader import PluginLoader

__all__ = [
    "PluginRegistry",
    "LifecycleManager",
    "ConfigManager",
    "PluginLoader",
]
