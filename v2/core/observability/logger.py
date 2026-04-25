"""
结构化日志记录器
"""

import logging
import json
from datetime import datetime


class StructuredLogger:
    """结构化日志记录器"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # 避免重复添加 handler
        if not self.logger.handlers:
            # JSON 格式化器
            handler = logging.StreamHandler()
            handler.setFormatter(self.JSONFormatter())
            self.logger.addHandler(handler)

    class JSONFormatter(logging.Formatter):
        """JSON 格式化器"""
        def format(self, record):
            log_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno
            }

            # 添加额外字段
            if hasattr(record, "request_id"):
                log_data["request_id"] = record.request_id
            if hasattr(record, "trace_id"):
                log_data["trace_id"] = record.trace_id
            if hasattr(record, "plugin"):
                log_data["plugin"] = record.plugin

            return json.dumps(log_data)

    def log(self, level: str, message: str, **kwargs):
        """记录日志"""
        log_func = getattr(self.logger, level.lower())
        log_func(message, extra=kwargs)

    def debug(self, message: str, **kwargs):
        """调试日志"""
        self.log("debug", message, **kwargs)

    def info(self, message: str, **kwargs):
        """信息日志"""
        self.log("info", message, **kwargs)

    def warning(self, message: str, **kwargs):
        """警告日志"""
        self.log("warning", message, **kwargs)

    def error(self, message: str, **kwargs):
        """错误日志"""
        self.log("error", message, **kwargs)

    def critical(self, message: str, **kwargs):
        """严重错误日志"""
        self.log("critical", message, **kwargs)
