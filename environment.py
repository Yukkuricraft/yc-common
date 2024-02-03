import re

from typing import Dict, List
from pprint import pformat
from functools import total_ordering

from src.common.config import load_toml_config
from src.common.config.config_node import ConfigNode
from src.common.logger_setup import logger
from src.common.paths import ServerPaths
from src.common.types import ServerTypes

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
        "config",
        "name",
        "hostname",
        "description",
        "alias",
        "formatted",
        "enable_env_protection",
    ]

    _config_node: ConfigNode

    @property
    def config_node(self) -> ConfigNode:
        """Returns a `ConfigNode` object representing the env config toml

        Returns:
            ConfigNode: Env config
        """
        return self._config_node
    @config_node.setter
    def config_node(self, node: ConfigNode):
        self._config_node = node

    @property
    def config(self) -> Dict:
        """Returns a `Dict` representing the env config toml

        Returns:
            Dict: Env config
        """
        return self.config_node.as_dict()

    @property
    def name(self) -> str:
        """Name of the env - usually in the format of env1, env2, env3, etc

        Returns:
            str: Name of env
        """
        return self.env_str

    @property
    def hostname(self) -> str:
        """The hostname of the docker container

        Returns:
            str: Hostname
        """
        general = self.config_node["general"] if "general" in self.config_node else {}
        return general["hostname"] if "hostname" in general else ""

    @property
    def description(self) -> str:
        """Description in the env config toml

        Returns:
            str: Description of the environment
        """
        general = self.config_node["general"] if "general" in self.config_node else {}
        return general["description"] if "description" in general else ""

    @property
    def alias(self) -> str:
        """A human-readable alias for the env (unlike 'env1', 'env2', etc)

        Returns:
            str: Alias
        """
        return self.load_runtime_env_var("ENV_ALIAS")

    @property
    def proxy_port(self) -> int:
        """Port that the Velocity proxy is running on.

        This is the port players connect to.

        Returns:
            int: Port number
        """
        return self.load_runtime_env_var("VELOCITY_PORT")

    @property
    def server_type(self) -> ServerTypes:
        """Returns the Minecraft server type

        Returns:
            ServerType
        """
        return self.load_runtime_env_var("MC_TYPE")

    @property
    def formatted(self) -> str:
        """A formatted name/string for the environment.

        Current returns format of:
            "Env {number} - {CapitalizedAlias}"

        Returns:
            str: Formatted string identifying the env.
        """
        return f"Env {self.num} - {self.alias.capitalize()}"

    @property
    def world_groups(self) -> List[str]:
        """A list of enabled world groups

        Returns:
            List[str]: A list of strings each representing a logical "world group".
        """
        all_world_groups = self.config_node["world-groups"].get_or_default(
            "enabled_groups", []
        )
        filtered_world_groups = list(
            filter(lambda w: w not in self.WORLDGROUP_NAME_BLOCKLIST, all_world_groups)
        )
        return filtered_world_groups

    @property
    def enable_env_protection(self) -> bool:
        """Returns whether env protection is enabled for this env.

        Environments with env protection cannot be deleted. It's effectively a deletion protection flag.

        Returns:
            bool: Whether env is protected or not.
        """
        general = self.config_node["general"] if "general" in self.config_node else {}
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

        self.config_node = load_toml_config(
            ServerPaths.get_env_toml_config_path(self.env_str), no_cache=True
        )
        self.envvars = self.config_node["runtime-environment-variables"]

    @classmethod
    def is_valid_env(cls, env_str: str) -> bool:
        """Returns whether env identifier string is valid.

        Currently we require a format of `env#` where # is any number. Eg, `env1`, `env99`, `env666`

        Args:
            env_str (str): Env name

        Returns:
            bool: Whether env name is valid.
        """
        return re.match("env\d+", env_str) is not None

    @classmethod
    def env_exists(cls, env_str: str) -> bool:
        """Checks if an env toml config with the matching env identifier string exists.

        Args:
            env_str (str): Env to check the config's existence for.

        Returns:
            bool: Whether env exists or not.
        """
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
        return self.config_node["runtime-environment-variables"].get_or_default(env_var, "")

    def to_json(self):
        return {field: getattr(self, field) for field in self.fields_to_print}

    def is_prod(self):
        # TODO: Maybe make an explicit flag? It'd end up effectively being an
        #       alias to `enable_env_protection, though. Two configs with similar
        #       meanings are blegh`
        return self.name == "env1"