#!/usr/bin/env python3

from typing import TextIO, Dict, Optional
from pathlib import Path
from pprint import pprint

import yaml  # type: ignore

yaml.SafeDumper.add_representer(
    type(None),
    lambda dumper, value: dumper.represent_scalar("tag:yaml.org,2002:null", ""),
)

from src.common.config.config_node import ConfigNode
from src.common.config.config_finder import ConfigFinder
from src.common.logger_setup import logger


class YamlConfig(ConfigNode):
    data: Dict
    config_path: Path

    def __init__(
        self, config_path: Optional[str] = None, base_path: Optional[Path] = None
    ):
        self.config_path = ConfigFinder(config_path, base_path).config_path

        with open(self.config_path, "r") as f:
            self.data = yaml.safe_load(f)

        if self.data == None:
            self.data = {}

        logger.info(self.config_path)
        logger.info(self.data)

        super().__init__(self.data)

    def print_config(self):
        pprint(self.data)

    @staticmethod
    def write_cb(f: TextIO, config: Dict):
        """Yaml config write callback.

        Writes with `f.write(yaml.safe_dump())`

        Args:
            f (TextIO): File object to write to
            config (dict): Config to dump
        """
        f.write(
            yaml.safe_dump(
                config,
                default_flow_style=False,
                sort_keys=False,
            ).encode("utf8")
        )
