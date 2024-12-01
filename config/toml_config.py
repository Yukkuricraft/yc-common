#!/usr/bin/env python3

from typing import Dict, Optional
from pathlib import Path
from pprint import pprint

import toml  # type: ignore
import tomli_w

from src.common.helpers import log_exception
from src.common.config.config_node import ConfigNode
from src.common.config.config_finder import ConfigFinder


class TomlConfig(ConfigNode):
    data: Dict

    def __init__(self, config_content: str):
        try:
            self.data = toml.loads(config_content)
        except:
            log_exception()

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
