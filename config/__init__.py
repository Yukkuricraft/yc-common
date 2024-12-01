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
        try:
            with open(config_path, "r") as f:
                __TOML_CONFIG[config_path] = TomlConfig(f.read())
        except:
            log_exception()

    return __TOML_CONFIG[config_path]


def load_env_config(
    config_path: Path,
    no_cache: bool = False,
) -> EnvConfig:
    global __ENV_CONFIG

    if config_path not in __ENV_CONFIG or __ENV_CONFIG[config_path] is None or no_cache:
        try:
            with open(config_path, "r") as f:
                __ENV_CONFIG[config_path] = EnvConfig(f.read())
        except:
            log_exception()

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
        try:
            with open(config_path, "r") as f:
                __YAML_CONFIG[config_path] = YamlConfig(f.read())
        except:
            log_exception()

    return __YAML_CONFIG[config_path]
