#!/usr/bin/env python3

from typing import TextIO, Dict, Optional
from pathlib import Path
from pprint import pprint, pformat

from src.common.helpers import log_exception
from src.common.config.config_node import ConfigNode
from src.common.logger_setup import logger


class EnvConfig(ConfigNode):
    data: Dict

    def __init__(self, config_content: str):
        self.data = {}

        try:
            for line in config_content.split("\n"):
                line = line.strip()
                if not line:
                    continue
                split = line.split("=")
                key = split[0]
                val = "=".join(
                    split[1:]
                )  # Just incase there were any ='s in the vals...? Is that even valid syntax?

                self.data[key] = val
        except:
            log_exception()

        if self.data == None:
            self.data = {}

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
        logger.debug(pformat(config))
        for key, value in config.items():
            if quote:
                f.write(f'{key}="{value}"\n'.encode("utf8"))
            else:
                f.write(f"{key}={value}\n".encode("utf8"))
