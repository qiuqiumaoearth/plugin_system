"""
插件注册表 - 线程安全的插件管理
"""

from typing import Dict, List, Optional, Any
from threading import RLock
import time

from core.base import PluginBase, PluginStatus


class PluginRegistry:
    """插件注册表"""

    def __init__(self):
        self._plugins: Dict[str, Dict[str, Any]] = {}
        self._lock = RLock()

    def register(self, plugin: PluginBase) -> bool:
        """注册插件"""
        with self._lock:
            metadata = plugin.metadata()
            plugin_name = metadata.name

            if plugin_name in self._plugins:
                # 检查版本是否更新
                existing_version = self._plugins[plugin_name]['metadata'].version
                if metadata.version <= existing_version:
                    return False

            self._plugins[plugin_name] = {
                'instance': plugin,
                'metadata': metadata,
                'status': plugin.get_status(),
                'enabled': True,
                'registered_at': time.time(),
                'last_executed_at': None,
                'execution_count': 0,
                'error_count': 0,
                'last_error': None
            }

            return True

    def unregister(self, plugin_name: str) -> bool:
        """注销插件"""
        with self._lock:
            if plugin_name in self._plugins:
                del self._plugins[plugin_name]
                return True
            return False

    def get(self, plugin_name: str) -> Optional[PluginBase]:
        """获取插件实例"""
        with self._lock:
            if plugin_name in self._plugins:
                return self._plugins[plugin_name]['instance']
            return None

    def get_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """获取插件详细信息"""
        with self._lock:
            return self._plugins.get(plugin_name)

    def list_all(self) -> List[str]:
        """列出所有插件名称"""
        with self._lock:
            return list(self._plugins.keys())

    def list_enabled(self) -> List[str]:
        """列出所有启用的插件"""
        with self._lock:
            return [name for name, info in self._plugins.items()
                   if info['enabled']]

    def enable(self, plugin_name: str) -> bool:
        """启用插件"""
        with self._lock:
            if plugin_name in self._plugins:
                self._plugins[plugin_name]['enabled'] = True
                return True
            return False

    def disable(self, plugin_name: str) -> bool:
        """禁用插件"""
        with self._lock:
            if plugin_name in self._plugins:
                self._plugins[plugin_name]['enabled'] = False
                return True
            return False

    def is_enabled(self, plugin_name: str) -> bool:
        """检查插件是否启用"""
        with self._lock:
            if plugin_name in self._plugins:
                return self._plugins[plugin_name]['enabled']
            return False

    def update_status(self, plugin_name: str, status: PluginStatus) -> None:
        """更新插件状态"""
        with self._lock:
            if plugin_name in self._plugins:
                self._plugins[plugin_name]['status'] = status

    def record_execution(self, plugin_name: str, success: bool, error: Optional[Exception] = None) -> None:
        """记录插件执行情况"""
        with self._lock:
            if plugin_name in self._plugins:
                info = self._plugins[plugin_name]
                info['last_executed_at'] = time.time()
                info['execution_count'] += 1

                if not success:
                    info['error_count'] += 1
                    info['last_error'] = str(error) if error else None

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._lock:
            return {
                'total_plugins': len(self._plugins),
                'enabled_plugins': len(self.list_enabled()),
                'disabled_plugins': len(self._plugins) - len(self.list_enabled()),
                'plugins': {
                    name: {
                        'execution_count': info['execution_count'],
                        'error_count': info['error_count'],
                        'error_rate': info['error_count'] / max(info['execution_count'], 1),
                        'status': info['status'].value,
                        'enabled': info['enabled']
                    }
                    for name, info in self._plugins.items()
                }
            }
