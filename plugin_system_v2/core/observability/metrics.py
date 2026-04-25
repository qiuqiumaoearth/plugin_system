"""
指标采集器（Prometheus 格式）
"""

from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest


class MetricsCollector:
    """指标采集器"""

    def __init__(self):
        self.registry = CollectorRegistry()

        # 插件执行计数
        self.execution_counter = Counter(
            "plugin_executions_total",
            "Total plugin executions",
            ["plugin", "status"],
            registry=self.registry
        )

        # 插件执行时间
        self.execution_duration = Histogram(
            "plugin_execution_duration_seconds",
            "Plugin execution duration",
            ["plugin"],
            registry=self.registry
        )

        # 当前活跃插件数
        self.active_plugins = Gauge(
            "active_plugins",
            "Number of active plugins",
            registry=self.registry
        )

        # 插件错误计数
        self.error_counter = Counter(
            "plugin_errors_total",
            "Total plugin errors",
            ["plugin", "error_type"],
            registry=self.registry
        )

        # API 请求计数
        self.api_requests = Counter(
            "api_requests_total",
            "Total API requests",
            ["endpoint", "method", "status"],
            registry=self.registry
        )

        # API 请求时长
        self.api_duration = Histogram(
            "api_request_duration_seconds",
            "API request duration",
            ["endpoint"],
            registry=self.registry
        )

    def record_execution(self, plugin_name: str, duration: float, success: bool):
        """记录执行"""
        status = "success" if success else "failure"
        self.execution_counter.labels(plugin=plugin_name, status=status).inc()
        self.execution_duration.labels(plugin=plugin_name).observe(duration)

    def record_error(self, plugin_name: str, error_type: str):
        """记录错误"""
        self.error_counter.labels(plugin=plugin_name, error_type=error_type).inc()

    def set_active_plugins(self, count: int):
        """设置活跃插件数"""
        self.active_plugins.set(count)

    def record_api_request(self, endpoint: str, method: str, status: int, duration: float):
        """记录 API 请求"""
        self.api_requests.labels(endpoint=endpoint, method=method, status=status).inc()
        self.api_duration.labels(endpoint=endpoint).observe(duration)

    def record(self, name: str, value: float, tags: dict = None):
        """通用记录方法"""
        # 简化的通用记录接口
        pass

    def get_metrics(self) -> bytes:
        """获取 Prometheus 格式的指标"""
        return generate_latest(self.registry)
