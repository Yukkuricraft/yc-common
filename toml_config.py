#!/usr/bin/env python3

from typing import Dict, Optional
from pathlib import Path
from pprint import pprint

import toml  # type: ignore

from src.common.config_node import ConfigNode
from src.common.config_finder import ConfigFinder


class TomlConfig(ConfigNode):
    data: Dict
    config_path: Path

    def __init__(
        self, config_path: Optional[str] = None, base_path: Optional[Path] = None
    ):
        self.config_path = ConfigFinder(config_path, base_path).config_path

        with open(self.config_path, "r") as f:
            self.data = toml.loads(f.read())

        super().__init__(self.data)

    def print_config(self):
        pprint(self.data)
