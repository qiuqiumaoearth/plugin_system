#!/usr/bin/env python3
"""
插件化执行系统 v2 - 主程序入口
"""

import asyncio
import signal
import sys
from pathlib import Path

from core.management.registry import PluginRegistry
from core.management.lifecycle import LifecycleManager
from core.management.config import ConfigManager
from core.management.loader import PluginLoader
from core.execution.executor import PluginExecutor
from core.execution.scheduler import PluginScheduler
from core.observability.logger import StructuredLogger
from core.observability.metrics import MetricsCollector
from api.http_server import HTTPServer


class PluginSystem:
    """插件系统主类"""

    def __init__(self, config_file: str = "config/system.yaml"):
        self.config = ConfigManager(config_file)
        self.logger = StructuredLogger("PluginSystem")
        self.metrics = MetricsCollector()

        # 初始化核心组件
        self.registry = PluginRegistry()
        self.lifecycle = LifecycleManager(self.registry)
        self.executor = PluginExecutor(self.registry)
        self.scheduler = PluginScheduler(self.executor)

        # 插件加载器
        plugin_dirs = self.config.get("plugins.directories", ["plugins/builtin"])
        self.loader = PluginLoader(plugin_dirs, self.registry)

        # API 服务器
        self.http_server = None

    def start(self):
        """启动系统"""
        self.logger.log("info", "Starting Plugin System v2...")

        # 1. 加载插件
        self._load_plugins()

        # 2. 初始化插件
        self._initialize_plugins()

        # 3. 启动 API 服务器
        self._start_api_server()

        self.logger.log("info", "Plugin System v2 started successfully")
        self.logger.log("info", f"API Server: http://localhost:{self.config.get('api.port', 8080)}")
        self.logger.log("info", f"Metrics: http://localhost:{self.config.get('metrics.port', 9090)}/metrics")

    def _load_plugins(self):
        """加载插件"""
        self.logger.log("info", "Loading plugins...")

        plugins = self.loader.discover_plugins()
        self.logger.log("info", f"Discovered {len(plugins)} plugin(s)")

        for plugin_path in plugins:
            plugin = self.loader.load_plugin(plugin_path)
            if plugin:
                self.logger.log("info", f"Loaded plugin: {plugin.metadata().name} v{plugin.metadata().version}")

        # 更新指标
        self.metrics.set_active_plugins(len(self.registry.list_all()))

    def _initialize_plugins(self):
        """初始化插件"""
        self.logger.log("info", "Initializing plugins...")

        for plugin_name in self.registry.list_all():
            plugin_config = self.config.get(f"plugins.{plugin_name}.config", {})
            success = self.lifecycle.initialize_plugin(plugin_name, plugin_config)

            if success:
                self.logger.log("info", f"Initialized plugin: {plugin_name}")
            else:
                self.logger.log("error", f"Failed to initialize plugin: {plugin_name}")

    def _start_api_server(self):
        """启动 API 服务器"""
        host = self.config.get("api.host", "0.0.0.0")
        port = self.config.get("api.port", 8080)

        self.http_server = HTTPServer(
            host=host,
            port=port,
            registry=self.registry,
            scheduler=self.scheduler,
            config=self.config
        )

        self.http_server.start()

    def stop(self):
        """停止系统"""
        self.logger.log("info", "Stopping Plugin System v2...")

        # 1. 停止 API 服务器
        if self.http_server:
            self.http_server.stop()

        # 2. 停止所有插件
        for plugin_name in self.registry.list_all():
            self.lifecycle.stop_plugin(plugin_name)

        self.logger.log("info", "Plugin System v2 stopped")


def signal_handler(signum, frame):
    """信号处理器"""
    print("\nReceived signal, shutting down...")
    sys.exit(0)


def main():
    """主函数"""
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 创建并启动系统
    system = PluginSystem()

    try:
        system.start()

        # 保持运行
        print("\nPlugin System v2 is running. Press Ctrl+C to stop.")
        while True:
            import time
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        system.stop()


if __name__ == "__main__":
    main()
