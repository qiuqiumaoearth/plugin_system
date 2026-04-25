"""
插件基类与接口定义
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List, AsyncIterator
from enum import Enum
import asyncio


class PluginType(Enum):
    """插件类型"""
    PROCESSOR = "processor"      # 数据处理插件
    FILTER = "filter"            # 数据过滤插件
    TRANSFORMER = "transformer"  # 数据转换插件
    AGGREGATOR = "aggregator"    # 数据聚合插件
    SINK = "sink"                # 数据输出插件


class PluginStatus(Enum):
    """插件状态"""
    UNLOADED = "unloaded"        # 未加载
    LOADING = "loading"          # 加载中
    LOADED = "loaded"            # 已加载
    INITIALIZING = "initializing" # 初始化中
    READY = "ready"              # 就绪
    RUNNING = "running"          # 运行中
    STOPPING = "stopping"        # 停止中
    STOPPED = "stopped"          # 已停止
    ERROR = "error"              # 错误
    DISABLED = "disabled"        # 已禁用


@dataclass
class PluginMetadata:
    """插件元数据"""
    name: str                           # 插件名称
    version: str                        # 插件版本（语义化版本）
    type: PluginType                    # 插件类型
    description: str                    # 插件描述
    author: str                         # 作者
    license: str                        # 许可证
    homepage: Optional[str] = None      # 主页
    repository: Optional[str] = None    # 代码仓库

    # 依赖声明
    dependencies: List[str] = field(default_factory=list)  # 插件依赖列表
    python_requires: str = ">=3.9"      # Python 版本要求
    system_requires: List[str] = field(default_factory=list)  # 系统依赖

    # 资源需求
    min_memory_mb: int = 128            # 最小内存需求（MB）
    max_memory_mb: int = 512            # 最大内存限制（MB）
    min_cpu_cores: float = 0.1          # 最小 CPU 核心数
    max_cpu_cores: float = 1.0          # 最大 CPU 核心数
    timeout_seconds: int = 30           # 默认超时时间（秒）

    # 能力声明
    supports_async: bool = False        # 是否支持异步执行
    supports_batch: bool = False        # 是否支持批量处理
    supports_streaming: bool = False    # 是否支持流式处理
    is_stateful: bool = False           # 是否有状态

    # 配置模式
    config_schema: Optional[Dict] = None  # JSON Schema 格式的配置模式

    # 标签与分类
    tags: List[str] = field(default_factory=list)  # 标签
    category: str = "general"           # 分类


class PluginBase(ABC):
    """插件基类 - 所有插件必须继承此类"""

    def __init__(self):
        self._metadata: Optional[PluginMetadata] = None
        self._config: Dict[str, Any] = {}
        self._status: PluginStatus = PluginStatus.UNLOADED
        self._context: Optional['PluginContext'] = None

    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """返回插件元数据"""
        pass

    # ========== 生命周期钩子 ==========

    def on_load(self) -> None:
        """插件加载时调用（仅一次）"""
        pass

    def on_init(self, config: Dict[str, Any]) -> None:
        """插件初始化时调用，传入配置"""
        self._config = config

    def on_start(self) -> None:
        """插件启动时调用"""
        pass

    def on_stop(self) -> None:
        """插件停止时调用"""
        pass

    def on_destroy(self) -> None:
        """插件销毁时调用（清理资源）"""
        pass

    def on_error(self, error: Exception) -> None:
        """插件执行出错时调用"""
        pass

    def on_config_change(self, new_config: Dict[str, Any]) -> None:
        """配置热更新时调用"""
        self._config = new_config

    # ========== 健康检查 ==========

    def health_check(self) -> Dict[str, Any]:
        """健康检查，返回健康状态"""
        return {
            "status": "healthy",
            "plugin": self.metadata().name,
            "version": self.metadata().version,
            "uptime": 0
        }

    # ========== 核心执行方法 ==========

    @abstractmethod
    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """同步执行方法（必须实现）"""
        pass

    async def run_async(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """异步执行方法（可选实现）"""
        # 默认实现：在线程池中执行同步方法
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.run, data)

    def run_batch(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量执行方法（可选实现）"""
        # 默认实现：逐个执行
        return [self.run(data) for data in data_list]

    async def run_stream(self, data_stream) -> AsyncIterator[Dict[str, Any]]:
        """流式执行方法（可选实现）"""
        async for data in data_stream:
            yield await self.run_async(data)

    # ========== 辅助方法 ==========

    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self._config.get(key, default)

    def set_status(self, status: PluginStatus) -> None:
        """设置插件状态"""
        self._status = status

    def get_status(self) -> PluginStatus:
        """获取插件状态"""
        return self._status

    def get_context(self) -> 'PluginContext':
        """获取插件上下文"""
        return self._context

    def set_context(self, context: 'PluginContext') -> None:
        """设置插件上下文"""
        self._context = context
