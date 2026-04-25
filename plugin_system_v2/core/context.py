"""
插件执行上下文
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import uuid


@dataclass
class PluginContext:
    """插件执行上下文"""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    span_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None        # 用户 ID
    tenant_id: Optional[str] = None      # 租户 ID

    # 执行环境
    execution_mode: str = "sync"         # 执行模式：sync/async/batch/stream
    timeout: int = 30                    # 超时时间（秒）
    retry_count: int = 0                 # 重试次数

    # 共享数据
    shared_data: Dict[str, Any] = field(default_factory=dict)

    # 日志与监控
    logger: Optional[Any] = None         # 日志记录器
    metrics: Optional[Any] = None        # 指标采集器
    tracer: Optional[Any] = None         # 追踪器

    # 资源限制
    max_memory_mb: int = 512             # 最大内存限制
    max_cpu_percent: float = 100.0       # 最大 CPU 使用率

    def log(self, level: str, message: str, **kwargs):
        """记录日志"""
        if self.logger:
            self.logger.log(level, message,
                          request_id=self.request_id,
                          trace_id=self.trace_id,
                          **kwargs)

    def record_metric(self, name: str, value: float, tags: Dict[str, str] = None):
        """记录指标"""
        if self.metrics:
            self.metrics.record(name, value, tags or {})

    def start_span(self, name: str):
        """开始一个追踪 Span"""
        if self.tracer:
            return self.tracer.start_span(name, parent_span_id=self.span_id)
        return None
