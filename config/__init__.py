#!/usr/bin/env python

import yaml  # type: ignore
from pprint import pprint, pformat
from pathlib import Path

from typing import Optional, Dict, List, Tuple

from src.common.config.config_finder import ConfigFinder
from src.common.config.config_node import ConfigNode
from src.common.config.env_config import EnvConfig
from src.common.config.yaml_config import YamlConfig
from src.common.config.toml_config import TomlConfig


__TOML_CONFIG: dict = {}
__YAML_CONFIG: dict = {}
__ENV_CONFIG: dict = {}


def load_toml_config(
    config_name: Optional[str] = None,
    base_path: Optional[Path] = None,
    no_cache: bool = False,
) -> TomlConfig:

    global __TOML_CONFIG

    if (
        config_name not in __TOML_CONFIG
        or __TOML_CONFIG[config_name] is None
        or no_cache
    ):
        __TOML_CONFIG[config_name] = TomlConfig(
            config_name,
            base_path,
        )

    return __TOML_CONFIG[config_name]


def load_env_config(
    config_name: Optional[str] = None,
    base_path: Optional[Path] = None,
    no_cache: bool = False,
) -> Dict[str, str]:
    global __ENV_CONFIG

    if config_name not in __ENV_CONFIG or __ENV_CONFIG[config_name] is None or no_cache:
        __ENV_CONFIG[config_name] = EnvConfig(config_name, base_path)

    return __ENV_CONFIG[config_name]


def load_yaml_config(
    config_name: Optional[str] = None,
    base_path: Optional[Path] = None,
    no_cache: bool = False,
) -> YamlConfig:
    global __YAML_CONFIG

    if (
        config_name not in __YAML_CONFIG
        or __YAML_CONFIG[config_name] is None
        or no_cache
    ):
        __YAML_CONFIG[config_name] = YamlConfig(
            config_name,
            base_path,
        )

    return __YAML_CONFIG[config_name]
