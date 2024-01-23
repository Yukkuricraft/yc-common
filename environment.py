import re

from pprint import pformat
from functools import total_ordering

from src.common.config import load_toml_config
from src.common.logger_setup import logger
from src.common.paths import ServerPaths

class InvalidPortException(Exception):
    pass

class InvalidEnvException(Exception):
    pass

@total_ordering
class Env:
    WORLDGROUP_NAME_BLOCKLIST = [
        "defaultconfigs",  # :`) Ugly folder structures yay`
    ]

    fields_to_print = [
        "config_as_dict",
        "name",
        "hostname",
        "description",
        "alias",
        "formatted",
        "enable_env_protection",
    ]

    config: dict

    @property
    def config_as_dict(self):
        return self.config.as_dict()

    @property
    def name(self):
        return self.env_str

    @property
    def hostname(self):
        general = self.config["general"] if "general" in self.config else {}
        return general["hostname"] if "hostname" in general else ""

    @property
    def description(self):
        general = self.config["general"] if "general" in self.config else {}
        return general["description"] if "description" in general else ""

    @property
    def alias(self):
        return self.load_runtime_env_var("ENV_ALIAS")

    @property
    def proxy_port(self):
        return self.load_runtime_env_var("VELOCITY_PORT")

    @property
    def formatted(self):
        return f"Env {self.num} - {self.alias.capitalize()}"

    @property
    def world_groups(self):
        all_world_groups = self.config["world-groups"].get_or_default(
            "enabled_groups", []
        )
        filtered_world_groups = list(
            filter(lambda w: w not in self.WORLDGROUP_NAME_BLOCKLIST, all_world_groups)
        )
        return filtered_world_groups

    @property
    def enable_env_protection(self):
        general = self.config["general"] if "general" in self.config else {}
        return (
            general["enable_env_protection"]
            if "enable_env_protection" in general
            else False
        )

    def __init__(self, env_str: str):
        if not self.is_valid_env(env_str):
            raise InvalidEnvException()

        logger.info(f"Instantiating Env object for env: '{env_str}'")

        self.env_str = env_str

        num = re.sub(r"\D", "", env_str)
        self.num = int(num) if num != "" else None

        self.config = load_toml_config(
            ServerPaths.get_env_toml_config_path(self.env_str), no_cache=True
        )
        self.envvars = self.config["runtime-environment-variables"]

    @classmethod
    def is_valid_env(cls, env_str: str) -> bool:
        return re.match("env\d+", env_str) is not None

    @classmethod
    def env_exists(cls, env_str: str) -> bool:
        return ServerPaths.get_env_toml_config_path(env_str).exists()

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        # Do we want to support non-prod/dev envs in the future?
        if self.name == "env1":
            return True

        return self.name < other.name

    def __repr__(self):
        entries = []
        for field in self.fields_to_print:
            entries.append(f" {field}: '{pformat(getattr(self, field))}'")

        return "{" + ",".join(entries) + "}"

    def load_runtime_env_var(self, env_var: str):
        return self.config["runtime-environment-variables"].get_or_default(env_var, "")

    def to_json(self):
        return {field: getattr(self, field) for field in self.fields_to_print}

    def is_prod(self):
        # TODO: Maybe make an explicit flag? It'd end up effectively being an
        #       alias to `enable_env_protection, though. Two configs with similar
        #       meanings are blegh`
        return self.name == "env1"