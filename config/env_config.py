#!/usr/bin/env python3

from typing import TextIO, Dict, Optional
from pathlib import Path
from configparser import ConfigParser
from pprint import pprint, pformat

from src.common.config.config_node import ConfigNode
from src.common.config.config_finder import ConfigFinder
from src.common.logger_setup import logger


class EnvConfig(ConfigNode):
    data: Dict
    config_path: Path

    def __init__(
        self, config_path: Optional[str] = None, base_path: Optional[Path] = None
    ):
        self.config_path = ConfigFinder(config_path, base_path).config_path

        self.data = {}
        with open(self.config_path, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                split = line.split("=")
                key = split[0]
                val = "=".join(
                    split[1:]
                )  # Just incase there were any ='s in the vals...? Is that even valid syntax?

                self.data[key] = val

        if self.data == None:
            self.data = {}

        logger.info(self.config_path)
        logger.info(self.data)

        super().__init__(self.data)

    def print_config(self):
        pprint(self.data)

    @staticmethod
    def write_cb(f: TextIO, config: Dict, quote: Optional[bool] = True):
        """Env config write callback.

        Args:
            f (TextIO): File object to write to
            config (dict): Config to dump
            quote (Optional[bool]) Whether to quote the config vals. Defaults to True
        """
        logger.info(pformat(config))
        for key, value in config.items():
            if quote:
                f.write(f'{key}="{value}"\n'.encode("utf8"))
            else:
                f.write(f"{key}={value}\n".encode("utf8"))
