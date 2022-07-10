#!/usr/bin/env python

import yaml  # type: ignore
from pprint import pprint, pformat
from pathlib import Path

from typing import Optional, Dict, List, Tuple

from .config_finder import ConfigFinder
from .config_node import ConfigNode
from .yaml_config import YamlConfig


__YAML_CONFIG: dict = {}
__ENV_CONFIG: dict = {}


def load_env_config(config_name: Optional[str] = None) -> Dict[str, str]:
    global __ENV_CONFIG

    if config_name not in __ENV_CONFIG or __ENV_CONFIG[config_name] is None:
        path = ConfigFinder(config_name).config_path
        config: Dict = {}
        with open(path, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue

                key, value = line.split("=")
                config[key] = value

        __ENV_CONFIG[config_name] = config

    return __ENV_CONFIG[config_name]


def load_yaml_config(config_name: Optional[str] = None) -> YamlConfig:
    global __YAML_CONFIG

    if config_name not in __YAML_CONFIG or __YAML_CONFIG[config_name] is None:
        __YAML_CONFIG[config_name] = YamlConfig(
            None if config_name is None else config_name
        )

    return __YAML_CONFIG[config_name]
