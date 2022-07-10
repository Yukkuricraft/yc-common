#!/usr/bin/env python3

from typing import Dict, Optional
from pathlib import Path

import yaml  # type: ignore

from .config_node import ConfigNode
from .config_finder import ConfigFinder


class YamlConfig(ConfigNode):
    data: Dict
    config_path: Path

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = ConfigFinder(config_path).config_path

        with open(self.config_path, "r") as f:
            self.data = yaml.safe_load(f)

        super().__init__(self.data)

    def print_config(self):
        pprint(self.data)
