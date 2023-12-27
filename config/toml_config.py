#!/usr/bin/env python3

from typing import Dict, Optional
from pathlib import Path
from pprint import pprint

import toml  # type: ignore
import tomli_w

from src.common.config.config_node import ConfigNode
from src.common.config.config_finder import ConfigFinder


class TomlConfig(ConfigNode):
    data: Dict
    config_path: Path

    def __init__(
        self, config_path: Optional[str] = None, base_path: Optional[Path] = None
    ):
        self.config_path = ConfigFinder(config_path, base_path).config_path

        with open(self.config_path, "r") as f:
            self.data = toml.loads(f.read())

        if self.data is None:
            self.data = {}

        super().__init__(self.data)

    def print_config(self):
        pprint(self.data)

    @staticmethod
    def write_cb(f, config):
        """Toml config write callback.

        Writes with `tomli_w.dump()`

        Args:
            f (TextIO): File object to write to
            config (dict): Config to dump
        """
        tomli_w.dump(config, f, multiline_strings=True)