#!/usr/bin/env python3

from typing import Dict, Optional
from pathlib import Path


from logging import getLogger

logger = getLogger(__name__)


class ConfigFinder:
    data: Dict
    config_path: Path

    default_config_name: str = "config.yml"

    def __init__(
        self, config_name: Optional[str] = None, config_path: Optional[Path] = None
    ):
        config_name = (
            config_name if config_name is not None else self.default_config_name
        )
        config_path = config_path if config_path is not None else Path(__file__).parent

        self.config_path = self.rec_find_config(config_name, config_path)

    def rec_find_config(self, config_name: str, curr_dir: Path):
        logger.debug(f"{curr_dir} ?? {config_name}")
        if str(curr_dir) == "/":
            raise FileNotFoundError(f"Could not find a valid {config_name}.")

        # Assumes config.yml is either in currdir or in a ancestor dir.
        config_path = curr_dir / config_name
        if config_path.exists():
            return config_path
        else:
            return self.rec_find_config(config_name, curr_dir.parent)
