from typing import Any, Optional

from application.config.internal.config_manager import ConfigManager


class ConfigService:
    config_manager: ConfigManager = ConfigManager()

    @staticmethod
    def get(*, key: str, default: Optional[Any] = None) -> Any:
        return ConfigService.config_manager.get(key=key, default=default)
