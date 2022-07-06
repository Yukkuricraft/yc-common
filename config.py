#!/usr/bin/env python

import yaml  # type: ignore
from pprint import pprint, pformat
from pathlib import Path

from typing import Optional, Dict, List, Tuple


class ConfigNode:
    data: Dict

    def __getattr__(self, name):
        rtn = self.data[name]
        return rtn

    def __getitem__(self, name):
        return self.data[name]

    def __contains__(self, item):
        return item in self.data

    def __str__(self):
        lines = ["",]
        for key, val in self.data.items():
            if type(val) in [dict, list]:
                val_str = pformat(val)
            else:
                val_str = val
            lines += '{}: {}'.format(key, val_str).split('\n')
        return '\n    '.join(lines)

    def __repr__(self):
        return self.__str__()

    def listnodes(self) -> List[str]:
        return list(self.data.keys())

    def get_or_default(self, name, default=None):
        if name not in self.data:
            return default
        return self.__getitem__(name)

    def items(
        self,
    ) -> List[Tuple[str,]]:
        return list(self.data.items())  # type: ignore

    def __init__(self, data: Dict):
        self.data = {}

        for k, v in data.items():
            if type(v) in [int, float, str, bool, list]:
                self.data[k] = v
            elif v is not None:
                self.data[k] = ConfigNode(dict(v))
            else:
                self.data[k] = None

    def as_dict(self):
        rtn_dict = {}

        for key, value in self.data.items():
            if type(value) == ConfigNode:
                rtn_dict[key] = value.as_dict()
            else:
                rtn_dict[key] = value

        return rtn_dict


class Config(ConfigNode):
    data: Dict
    config_path: Path

    default_config_name: str = "config.yml"

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = (
            config_path if config_path is not None else self.get_default_config()
        )

        with open(self.config_path, "r") as f:
            self.data = yaml.safe_load(f)

        super().__init__(self.data)

    def get_default_config(self, curr_dir: Optional[Path] = None):
        if str(curr_dir) == "/":
            raise FileNotFoundError(
                f"Could not find a valid {self.default_config_name}."
            )

        if curr_dir is None:
            curr_dir = Path(__file__)

        # Assumes config.yml is either in currdir or in a ancestor dir.
        config_path = curr_dir / self.default_config_name
        if config_path.exists():
            return config_path
        else:
            return self.get_default_config(curr_dir.parent)

    def print_config(self):
        pprint(self.data)


__CONFIG: dict = {}


def get_config(config_path: Optional[str] = None) -> Config:
    global __CONFIG

    if config_path not in __CONFIG or __CONFIG[config_path] is None:
        __CONFIG[config_path] = Config(None if config_path is None else Path(config_path))

    return __CONFIG[config_path]
