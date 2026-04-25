"""
配置管理器 - 支持热更新
"""

import yaml
import json
from typing import Dict, Any, Optional, Callable, List
from pathlib import Path
import threading


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_file: str):
        self.config_file = Path(config_file)
        self._config: Dict[str, Any] = {}
        self._watchers: Dict[str, List[Callable]] = {}
        self._lock = threading.RLock()
        self._load_config()

    def _load_config(self):
        """加载配置文件"""
        if not self.config_file.exists():
            # 创建默认配置
            self._config = self._get_default_config()
            return

        with open(self.config_file, 'r', encoding='utf-8') as f:
            if self.config_file.suffix in ['.yaml', '.yml']:
                self._config = yaml.safe_load(f) or {}
            elif self.config_file.suffix == '.json':
                self._config = json.load(f)
            else:
                self._config = {}

    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            'api': {
                'host': '0.0.0.0',
                'port': 8080
            },
            'metrics': {
                'port': 9090
            },
            'plugins': {
                'directories': ['plugins/builtin', 'plugins/external'],
                'global': {
                    'max_concurrent': 10,
                    'default_timeout': 30,
                    'enable_metrics': True,
                    'enable_tracing': True
                }
            },
            'logging': {
                'level': 'INFO',
                'format': 'json'
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        with self._lock:
            keys = key.split('.')
            value = self._config

            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                    if value is None:
                        return default
                else:
                    return default

            return value

    def set(self, key: str, value: Any):
        """设置配置项"""
        with self._lock:
            keys = key.split('.')
            config = self._config

            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]

            config[keys[-1]] = value

            # 触发监听器
            self._notify_watchers(key, value)

    def watch(self, key: str, callback: Callable):
        """监听配置变化"""
        with self._lock:
            if key not in self._watchers:
                self._watchers[key] = []
            self._watchers[key].append(callback)

    def _notify_watchers(self, key: str, value: Any):
        """通知监听器"""
        if key in self._watchers:
            for callback in self._watchers[key]:
                try:
                    callback(key, value)
                except Exception as e:
                    print(f"Error in config watcher: {e}")

    def reload(self):
        """重新加载配置"""
        with self._lock:
            old_config = self._config.copy()
            self._load_config()

            # 检测变化并通知
            self._detect_changes(old_config, self._config)

    def _detect_changes(self, old: Dict, new: Dict, prefix: str = ""):
        """检测配置变化"""
        for key in new:
            full_key = f"{prefix}.{key}" if prefix else key

            if key not in old:
                self._notify_watchers(full_key, new[key])
            elif old[key] != new[key]:
                if isinstance(new[key], dict) and isinstance(old[key], dict):
                    self._detect_changes(old[key], new[key], full_key)
                else:
                    self._notify_watchers(full_key, new[key])

    def save(self):
        """保存配置到文件"""
        with self._lock:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_file, 'w', encoding='utf-8') as f:
                if self.config_file.suffix in ['.yaml', '.yml']:
                    yaml.dump(self._config, f, default_flow_style=False)
                elif self.config_file.suffix == '.json':
                    json.dump(self._config, f, indent=2)
