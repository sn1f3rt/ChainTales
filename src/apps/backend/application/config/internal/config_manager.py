from typing import Any, Dict, Optional

import os
from pathlib import Path

import yaml


class ConfigManager:
    CONFIG_FILE_PARENT_LEVEL: int = 6
    CONFIG_FILE_NAME: str = "config.yaml"

    def __init__(self) -> None:
        self.config_data: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        base_dir = Path(__file__).resolve().parents[self.CONFIG_FILE_PARENT_LEVEL]
        config_file_path = os.path.join(base_dir, self.CONFIG_FILE_NAME)

        try:
            with open(config_file_path, "r") as file:
                self.config_data = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file '{self.CONFIG_FILE_NAME}' not found."
            )

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        keys = key.split(".")
        value = self.config_data
        for k in keys:
            value = value.get(k, default)
            if value is default:
                break
        return value
