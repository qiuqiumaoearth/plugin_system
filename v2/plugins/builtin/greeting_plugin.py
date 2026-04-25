# -*- coding: utf-8 -*-
"""
问候插件 - 根据时间问候用户
"""

from core.base import PluginBase, PluginMetadata, PluginType
from typing import Dict, Any
from datetime import datetime


class GreetingPlugin(PluginBase):
    """问候插件"""

    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="greeting_plugin",
            version="1.0.0",
            type=PluginType.PROCESSOR,
            description="根据时间问候用户",
            author="Your Name",
            license="MIT",
            timeout_seconds=10,
            tags=["greeting", "example"]
        )

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """根据时间返回问候语"""
        # 获取用户名
        name = data.get("name", "朋友")

        # 获取当前小时
        hour = datetime.now().hour

        # 根据时间决定问候语
        if 5 <= hour < 12:
            greeting = f"早上好，{name}！"
            time_period = "早晨"
        elif 12 <= hour < 18:
            greeting = f"下午好，{name}！"
            time_period = "下午"
        else:
            greeting = f"晚上好，{name}！"
            time_period = "晚上"

        return {
            "greeting": greeting,
            "time_period": time_period,
            "hour": hour
        }
