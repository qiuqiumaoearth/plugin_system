"""
插件加载器
"""

from typing import List, Optional
import importlib.util
import inspect
import os
from pathlib import Path

from core.base import PluginBase, PluginStatus
from core.management.registry import PluginRegistry


class PluginLoader:
    """插件加载器"""

    def __init__(self, plugin_dirs: List[str], registry: PluginRegistry):
        self.plugin_dirs = plugin_dirs
        self.registry = registry
        self._loaded_plugins = {}

    def discover_plugins(self) -> List[str]:
        """发现所有可用插件"""
        plugins = []

        for plugin_dir in self.plugin_dirs:
            plugins.extend(self._scan_directory(plugin_dir))

        return plugins

    def _scan_directory(self, directory: str) -> List[str]:
        """扫描目录中的插件"""
        plugins = []

        if not os.path.exists(directory):
            return plugins

        for filename in os.listdir(directory):
            if filename.endswith('.py') and not filename.startswith('_'):
                plugin_path = os.path.join(directory, filename)
                plugins.append(plugin_path)

        return plugins

    def load_plugin(self, plugin_path: str) -> Optional[PluginBase]:
        """加载单个插件"""
        try:
            # 1. 动态导入模块
            module_name = f"plugin_{Path(plugin_path).stem}"
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)

            if spec is None or spec.loader is None:
                raise ValueError(f"Cannot load plugin from {plugin_path}")

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # 2. 查找插件类
            plugin_class = self._find_plugin_class(module)
            if not plugin_class:
                raise ValueError(f"No plugin class found in {plugin_path}")

            # 3. 实例化插件
            plugin_instance = plugin_class()

            # 4. 验证插件
            self._validate_plugin(plugin_instance)

            # 5. 调用加载钩子
            plugin_instance.on_load()
            plugin_instance.set_status(PluginStatus.LOADED)

            # 6. 注册插件
            plugin_name = plugin_instance.metadata().name
            self.registry.register(plugin_instance)
            self._loaded_plugins[plugin_name] = plugin_instance

            return plugin_instance

        except Exception as e:
            print(f"Failed to load plugin {plugin_path}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _find_plugin_class(self, module) -> Optional[type]:
        """在模块中查找插件类"""
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and
                issubclass(obj, PluginBase) and
                obj is not PluginBase):
                return obj
        return None

    def _validate_plugin(self, plugin: PluginBase) -> None:
        """验证插件是否符合规范"""
        # 检查必需方法
        if not hasattr(plugin, 'metadata'):
            raise ValueError("Plugin must implement metadata() method")

        if not hasattr(plugin, 'run'):
            raise ValueError("Plugin must implement run() method")

        # 检查元数据
        metadata = plugin.metadata()
        if not metadata.name:
            raise ValueError("Plugin must have a name")

        if not metadata.version:
            raise ValueError("Plugin must have a version")

    def unload_plugin(self, plugin_name: str) -> bool:
        """卸载插件"""
        if plugin_name not in self._loaded_plugins:
            return False

        plugin = self._loaded_plugins[plugin_name]

        try:
            # 调用销毁钩子
            plugin.on_destroy()
            plugin.set_status(PluginStatus.UNLOADED)

            # 从注册表移除
            self.registry.unregister(plugin_name)

            # 从缓存中移除
            del self._loaded_plugins[plugin_name]

            return True
        except Exception as e:
            print(f"Failed to unload plugin {plugin_name}: {e}")
            return False

    def reload_plugin(self, plugin_name: str, plugin_path: str) -> Optional[PluginBase]:
        """热重载插件"""
        # 1. 卸载旧版本
        self.unload_plugin(plugin_name)

        # 2. 加载新版本
        return self.load_plugin(plugin_path)

    def get_loaded_plugins(self) -> dict:
        """获取所有已加载的插件"""
        return self._loaded_plugins.copy()
