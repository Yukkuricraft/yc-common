#!/usr/bin/env python3

from typing import Dict, Optional
from pathlib import Path


class ConfigFinder:
    data: Dict
    config_path: Path

    default_config_name: str = "config.yml"

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = (
            self.rec_find_config(config_path, Path(__file__).parent)
            if config_path is not None
            else self.get_default_config()
        )

    def get_default_config(self):
        return self.rec_find_config(self.default_config_name, Path(__file__).parent)

    def rec_find_config(self, config_name: str, curr_dir: Path):
        if str(curr_dir) == "/":
            raise FileNotFoundError(f"Could not find a valid {config_name}.")

        # Assumes config.yml is either in currdir or in a ancestor dir.
        config_path = curr_dir / config_name
        if config_path.exists():
            return config_path
        else:
            return self.rec_find_config(config_name, curr_dir.parent)
