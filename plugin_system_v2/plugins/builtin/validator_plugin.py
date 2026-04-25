"""
Validator 插件 - 数据验证
"""

from core.base import PluginBase, PluginMetadata, PluginType
from typing import Dict, Any


class ValidatorPlugin(PluginBase):
    """Validator 插件"""

    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="validator_plugin",
            version="1.0.0",
            type=PluginType.FILTER,
            description="Validator plugin that validates input data",
            author="Plugin System Team",
            license="MIT",
            timeout_seconds=10,
            tags=["validation", "filter"]
        )

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """验证数据"""
        required_fields = self.get_config("required_fields", [])
        errors = []

        # 检查必需字段
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        # 检查数据类型
        if "age" in data and not isinstance(data["age"], int):
            errors.append("Field 'age' must be an integer")

        if "email" in data and "@" not in str(data["email"]):
            errors.append("Field 'email' must be a valid email address")

        is_valid = len(errors) == 0

        return {
            "valid": is_valid,
            "errors": errors,
            "data": data if is_valid else None
        }
