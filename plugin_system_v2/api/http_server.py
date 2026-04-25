"""
HTTP 服务器
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

from core.management.registry import PluginRegistry
from core.execution.scheduler import PluginScheduler
from core.context import PluginContext
from core.observability.logger import StructuredLogger
from core.observability.metrics import MetricsCollector


class HTTPServer:
    """HTTP API 服务器"""

    def __init__(self, host: str, port: int, registry: PluginRegistry,
                 scheduler: PluginScheduler, config):
        self.host = host
        self.port = port
        self.registry = registry
        self.scheduler = scheduler
        self.config = config
        self.logger = StructuredLogger("HTTPServer")

        # 创建 Flask 应用
        self.app = Flask(__name__)
        CORS(self.app)

        # 注册路由
        self._register_routes()

        # 服务器线程
        self.server_thread = None
        self.running = False

    def _register_routes(self):
        """注册路由"""

        @self.app.route('/health', methods=['GET'])
        def health():
            """健康检查"""
            return jsonify({"status": "healthy", "timestamp": time.time()})

        @self.app.route('/ready', methods=['GET'])
        def ready():
            """就绪检查"""
            return jsonify({"status": "ready", "plugins": len(self.registry.list_all())})

        @self.app.route('/api/v1/plugins', methods=['GET'])
        def list_plugins():
            """列出所有插件"""
            plugins = []
            for plugin_name in self.registry.list_all():
                info = self.registry.get_info(plugin_name)
                if info:
                    metadata = info['metadata']
                    plugins.append({
                        "name": metadata.name,
                        "version": metadata.version,
                        "type": metadata.type.value,
                        "description": metadata.description,
                        "enabled": info['enabled'],
                        "status": info['status'].value,
                        "execution_count": info['execution_count'],
                        "error_count": info['error_count']
                    })

            return jsonify({"plugins": plugins, "total": len(plugins)})

        @self.app.route('/api/v1/plugins/<plugin_name>', methods=['GET'])
        def get_plugin(plugin_name):
            """获取插件详情"""
            info = self.registry.get_info(plugin_name)
            if not info:
                return jsonify({"error": "Plugin not found"}), 404

            metadata = info['metadata']
            return jsonify({
                "name": metadata.name,
                "version": metadata.version,
                "type": metadata.type.value,
                "description": metadata.description,
                "author": metadata.author,
                "license": metadata.license,
                "enabled": info['enabled'],
                "status": info['status'].value,
                "execution_count": info['execution_count'],
                "error_count": info['error_count'],
                "last_error": info['last_error']
            })

        @self.app.route('/api/v1/plugins/<plugin_name>/enable', methods=['POST'])
        def enable_plugin(plugin_name):
            """启用插件"""
            success = self.registry.enable(plugin_name)
            if success:
                return jsonify({"message": f"Plugin {plugin_name} enabled"})
            return jsonify({"error": "Plugin not found"}), 404

        @self.app.route('/api/v1/plugins/<plugin_name>/disable', methods=['POST'])
        def disable_plugin(plugin_name):
            """禁用插件"""
            success = self.registry.disable(plugin_name)
            if success:
                return jsonify({"message": f"Plugin {plugin_name} disabled"})
            return jsonify({"error": "Plugin not found"}), 404

        @self.app.route('/api/v1/execute', methods=['POST'])
        def execute_plugin():
            """执行插件"""
            start_time = time.time()

            try:
                data = request.get_json()
                plugin_name = data.get('plugin')
                plugin_data = data.get('data', {})
                timeout = data.get('timeout', 30)

                if not plugin_name:
                    return jsonify({"error": "Missing 'plugin' field"}), 400

                # 创建上下文
                context = PluginContext(
                    timeout=timeout,
                    logger=self.logger,
                    metrics=self.scheduler.executor.registry
                )

                # 执行插件
                result = self.scheduler.executor.execute_with_timeout(
                    plugin_name, plugin_data, context, timeout
                )

                duration = time.time() - start_time

                return jsonify({
                    "success": result["success"],
                    "plugin": result["plugin"],
                    "result": result["result"],
                    "error": result["error"],
                    "duration": duration
                })

            except Exception as e:
                self.logger.error(f"API error: {str(e)}")
                return jsonify({"error": str(e)}), 500

        @self.app.route('/api/v1/execute/serial', methods=['POST'])
        def execute_serial():
            """串行执行多个插件"""
            try:
                data = request.get_json()
                plugins = data.get('plugins', [])
                plugin_data = data.get('data', {})

                if not plugins:
                    return jsonify({"error": "Missing 'plugins' field"}), 400

                context = PluginContext(logger=self.logger)
                results = self.scheduler.execute_serial(plugins, plugin_data, context)

                return jsonify({"results": results})

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route('/api/v1/execute/parallel', methods=['POST'])
        def execute_parallel():
            """并行执行多个插件"""
            try:
                data = request.get_json()
                plugins = data.get('plugins', [])
                plugin_data = data.get('data', {})

                if not plugins:
                    return jsonify({"error": "Missing 'plugins' field"}), 400

                context = PluginContext(logger=self.logger)
                results = self.scheduler.execute_parallel(plugins, plugin_data, context)

                return jsonify({"results": results})

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route('/api/v1/statistics', methods=['GET'])
        def get_statistics():
            """获取统计信息"""
            stats = self.registry.get_statistics()
            return jsonify(stats)

        @self.app.route('/metrics', methods=['GET'])
        def metrics():
            """Prometheus 指标"""
            # 这里需要从 main.py 传入 metrics collector
            return "# Metrics endpoint\n", 200, {'Content-Type': 'text/plain'}

    def start(self):
        """启动服务器"""
        self.running = True
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()
        self.logger.info(f"HTTP Server started on {self.host}:{self.port}")

    def _run_server(self):
        """运行服务器"""
        self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)

    def stop(self):
        """停止服务器"""
        self.running = False
        self.logger.info("HTTP Server stopped")
