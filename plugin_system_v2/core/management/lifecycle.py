"""
插件生命周期管理器
"""

from typing import Dict, Any

from core.base import PluginStatus
from core.management.registry import PluginRegistry


class LifecycleManager:
    """插件生命周期管理器"""

    def __init__(self, registry: PluginRegistry):
        self.registry = registry

    def initialize_plugin(self, plugin_name: str, config: Dict[str, Any]) -> bool:
        """初始化插件"""
        plugin = self.registry.get(plugin_name)
        if not plugin:
            return False

        try:
            plugin.set_status(PluginStatus.INITIALIZING)
            plugin.on_init(config)
            plugin.set_status(PluginStatus.READY)
            self.registry.update_status(plugin_name, PluginStatus.READY)
            return True
        except Exception as e:
            plugin.set_status(PluginStatus.ERROR)
            plugin.on_error(e)
            self.registry.update_status(plugin_name, PluginStatus.ERROR)
            return False

    def start_plugin(self, plugin_name: str) -> bool:
        """启动插件"""
        plugin = self.registry.get(plugin_name)
        if not plugin:
            return False

        try:
            plugin.on_start()
            plugin.set_status(PluginStatus.RUNNING)
            self.registry.update_status(plugin_name, PluginStatus.RUNNING)
            return True
        except Exception as e:
            plugin.on_error(e)
            return False

    def stop_plugin(self, plugin_name: str) -> bool:
        """停止插件"""
        plugin = self.registry.get(plugin_name)
        if not plugin:
            return False

        try:
            plugin.set_status(PluginStatus.STOPPING)
            plugin.on_stop()
            plugin.set_status(PluginStatus.STOPPED)
            self.registry.update_status(plugin_name, PluginStatus.STOPPED)
            return True
        except Exception as e:
            plugin.on_error(e)
            return False

    def destroy_plugin(self, plugin_name: str) -> bool:
        """销毁插件"""
        plugin = self.registry.get(plugin_name)
        if not plugin:
            return False

        try:
            plugin.on_destroy()
            plugin.set_status(PluginStatus.UNLOADED)
            return True
        except Exception as e:
            plugin.on_error(e)
            return False

    def reload_plugin_config(self, plugin_name: str, new_config: Dict[str, Any]) -> bool:
        """热更新插件配置"""
        plugin = self.registry.get(plugin_name)
        if not plugin:
            return False

        try:
            plugin.on_config_change(new_config)
            return True
        except Exception as e:
            plugin.on_error(e)
            return False
