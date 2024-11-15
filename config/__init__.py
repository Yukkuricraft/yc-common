#!/usr/bin/env python

import yaml  # type: ignore
from pathlib import Path

from typing import Optional

from src.common.config.config_finder import ConfigFinder
from src.common.config.config_node import ConfigNode
from src.common.config.env_config import EnvConfig
from src.common.config.yaml_config import YamlConfig
from src.common.config.toml_config import TomlConfig


__TOML_CONFIG: dict = {}
__YAML_CONFIG: dict = {}
__ENV_CONFIG: dict = {}


def load_toml_config(
    config_path: Path,
    no_cache: bool = False,
) -> TomlConfig:

    global __TOML_CONFIG

    if (
        config_path not in __TOML_CONFIG
        or __TOML_CONFIG[config_path] is None
        or no_cache
    ):
        __TOML_CONFIG[config_path] = TomlConfig(Path(config_path))

    return __TOML_CONFIG[config_path]


def load_env_config(
    config_path: Path,
    no_cache: bool = False,
) -> EnvConfig:
    global __ENV_CONFIG

    if config_path not in __ENV_CONFIG or __ENV_CONFIG[config_path] is None or no_cache:
        __ENV_CONFIG[config_path] = EnvConfig(Path(config_path))

    return __ENV_CONFIG[config_path]


def load_yaml_config(
    config_path: Path,
    no_cache: bool = False,
) -> YamlConfig:
    global __YAML_CONFIG

    if (
        config_path not in __YAML_CONFIG
        or __YAML_CONFIG[config_path] is None
        or no_cache
    ):
        __YAML_CONFIG[config_path] = YamlConfig(Path(config_path))

    return __YAML_CONFIG[config_path]
