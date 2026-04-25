"""
插件注册表单元测试
"""

import pytest
from core.management.registry import PluginRegistry
from core.base import PluginBase, PluginMetadata, PluginType, PluginStatus


class MockPlugin(PluginBase):
    """测试用模拟插件"""

    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="mock_plugin",
            version="1.0.0",
            type=PluginType.PROCESSOR,
            description="Mock plugin for testing",
            author="Test",
            license="MIT"
        )

    def run(self, data: dict) -> dict:
        return {"result": "mock"}


class TestPluginRegistry:
    """插件注册表测试"""

    def test_register_plugin(self):
        """测试注册插件"""
        registry = PluginRegistry()
        plugin = MockPlugin()

        success = registry.register(plugin)
        assert success is True
        assert "mock_plugin" in registry.list_all()

    def test_get_plugin(self):
        """测试获取插件"""
        registry = PluginRegistry()
        plugin = MockPlugin()
        registry.register(plugin)

        retrieved = registry.get("mock_plugin")
        assert retrieved is not None
        assert retrieved.metadata().name == "mock_plugin"

    def test_enable_disable_plugin(self):
        """测试启用/禁用插件"""
        registry = PluginRegistry()
        plugin = MockPlugin()
        registry.register(plugin)

        # 默认启用
        assert registry.is_enabled("mock_plugin") is True

        # 禁用
        registry.disable("mock_plugin")
        assert registry.is_enabled("mock_plugin") is False

        # 启用
        registry.enable("mock_plugin")
        assert registry.is_enabled("mock_plugin") is True

    def test_record_execution(self):
        """测试记录执行"""
        registry = PluginRegistry()
        plugin = MockPlugin()
        registry.register(plugin)

        # 记录成功执行
        registry.record_execution("mock_plugin", True)
        info = registry.get_info("mock_plugin")
        assert info['execution_count'] == 1
        assert info['error_count'] == 0

        # 记录失败执行
        registry.record_execution("mock_plugin", False, Exception("test error"))
        info = registry.get_info("mock_plugin")
        assert info['execution_count'] == 2
        assert info['error_count'] == 1

    def test_get_statistics(self):
        """测试获取统计信息"""
        registry = PluginRegistry()
        plugin = MockPlugin()
        registry.register(plugin)

        stats = registry.get_statistics()
        assert stats['total_plugins'] == 1
        assert stats['enabled_plugins'] == 1
        assert 'mock_plugin' in stats['plugins']
