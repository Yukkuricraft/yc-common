from pathlib import Path
from typing import Optional

from src.common.types import ConfigType
from src.generator.constants import BASE_DATA_PATH, REPO_ROOT_PATH


class ServerPaths:

    ## Repo based directory helpers

    @staticmethod
    def get_generated_configs_path(env: str) -> Path:
        """Get the path we dump all env-based generated files

        Equivalent to `{constants.REPO_ROOT_PATH}/gen`

        Think files like velocity configs, env files, docker compose files

        Args:
            env (str): Environment name string

        Returns:
            Path: Generated files path
        """
        return REPO_ROOT_PATH / "gen"

    @staticmethod
    def get_env_toml_config_dir_path() -> Path:
        """Get the path we expect the env toml configs to be in

        Equivalent to `{constants.REPO_ROOT_PATH}/env`

        Args:
            env (str): Environment name string

        Returns:
            Path: Dir path where we keep our env tomls
        """
        return REPO_ROOT_PATH / "env"

    ## Base data path based directory helpers

    @staticmethod
    def get_env_data_path(env: str) -> Path:
        """Get the base data path for a given `env`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}`

        Args:
            env (str): Environment name string

        Returns:
            Path: Base data path for `env`
        """
        return BASE_DATA_PATH / "env" / env

    @staticmethod
    def get_env_default_configs_path(env: str) -> Path:
        """Get the default configs path for a given `env`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/defaultconfigs`

        Args:
            env (str): Environment name string

        Returns:
            Path: Default configs path
        """
        return ServerPaths.get_env_data_path(env) / "defaultconfigs"

    @staticmethod
    def get_env_and_world_group_path(env: str, world_group: str) -> Path:
        """Get the data path for a specific `env` and `world_group`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/{world_group}`

        Args:
            env (str): Environment name string
            world_group (str): World Group name. Eg, 'creative', 'survival', 'gensokyo'

        Returns:
            Path: Data path for `env` and `world_group`
        """
        return BASE_DATA_PATH / "env" / env / world_group

    @staticmethod
    def get_env_and_world_group_configs_path(env: str, world_group: str) -> Path:
        """Get the config data path for a specific `env` and `world_group`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/{world_group}/configs`

        Args:
            env (str): Environment name string
            world_group (str): World Group name. Eg, 'creative', 'survival', 'gensokyo'

        Returns:
            Path: Config path
        """
        return ServerPaths.get_env_and_world_group_path(env, world_group) / "configs"

    MODS_FILE_DIR = "mods"
    MODS_CONFIG_DIR = "mods"
    PLUGINS_CONFIG_DIR = "plugins"
    WORLDS_CONFIG_DIR = "server"

    @staticmethod
    def get_config_path(env: str, world_group: str, config_type: ConfigType) -> Path:
        """Get the configs path for a given `env`, `world_group`, and `config_type`.

        Normally:
        - Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/{world_group}/configs/{config_type_dirname}`

        Except for `ConfigType.MOD_FILES` because lol LuckPerms and generating files in the mod files directory:
        - Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/{world_group}/mods`

        Args:
            env (str): Environment name string
            world_group (str): World Group name. Eg, 'creative', 'survival', 'gensokyo'
            config_type (ConfigType): Config type to return path for

        Returns:
            Path: Config path
        """
        if config_type == ConfigType.MOD:
            return (
                ServerPaths.get_env_and_world_group_configs_path(env, world_group)
                / ServerPaths.MODS_CONFIG_DIR
            )
        elif config_type == ConfigType.PLUGIN:
            return (
                ServerPaths.get_env_and_world_group_configs_path(env, world_group)
                / ServerPaths.PLUGINS_CONFIG_DIR
            )
        elif config_type == ConfigType.SERVER:
            return (
                ServerPaths.get_env_and_world_group_configs_path(env, world_group)
                / ServerPaths.WORLDS_CONFIG_DIR
            )
        elif config_type == ConfigType.MOD_FILES:
            return (
                ServerPaths.get_env_and_world_group_path(env, world_group)
                / ServerPaths.MODS_FILE_DIR
            )

    ## Repo based specific filepath helpers

    @staticmethod
    def get_env_toml_config_path(env: str) -> Path:
        """Get the toml config path for `env`.

        Equivalent to `{constants.REPO_ROOT_PATH}/env/{env}.toml`

        Args:
            env (str): Environment name string

        Returns:
            Path: Env toml config path
        """
        return ServerPaths.get_env_toml_config_dir_path() / f"{env}.toml"

    @staticmethod
    def get_generated_docker_compose_path(env: str) -> Path:
        """Returns the `docker-compose-{env}.yml` path for a given `env`.

        Equivalent to `{constants.REPO_ROOT_PATH}/gen/docker-compose-{env}.yml`

        Args:
            env (str): Environment name string

        Returns:
            Path: Generated `docker-compose-{env}.yml` path
        """
        return ServerPaths.get_generated_configs_path(env) / f"docker-compose-{env}.yml"

    @staticmethod
    def get_generated_env_file_path(env: str) -> Path:
        """Returns the `{env}.env` path for a given `env`.

        Equivalent to `{constants.REPO_ROOT_PATH}/gen/{env}.env`

        Args:
            env (str): Environment name string

        Returns:
            Path: Generated `{env}.env` path
        """
        return ServerPaths.get_generated_configs_path(env) / f"{env}.env"

    @staticmethod
    def get_generated_velocity_config_path(env: str) -> Path:
        """Returns the `velocity-{env}.toml` path for a given `env`.

        Equivalent to `{constants.REPO_ROOT_PATH}/gen/velocity-{env}.toml`

        Args:
            env (str): Environment name string

        Returns:
            Path: Generated `velocity-{env}.toml` path
        """
        return ServerPaths.get_generated_configs_path(env) / f"velocity-{env}.toml"

    ## Base data path based specific filepath helpers

    @staticmethod
    def get_server_properties_path(env: str, world_group: str) -> Path:
        """Returns the `server.properties` path for a given `env` and `world_group`

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/{world_group}/configs/server/server.properties`

        Args:
            env (str): Environment name string
            world_group (str): World Group name. Eg, 'creative', 'survival', 'gensokyo'

        Returns:
            Path: Server.properties path
        """
        return (
            ServerPaths.get_config_path(env, world_group, ConfigType.SERVER)
            / "server.properties"
        )

    @staticmethod
    def get_paper_global_yml_path(env: str, world_group: Optional[str] = None) -> Path:
        """Returns the `paper-global.yml` path for a given `env` and optional `world_group`

        If `world_group` supplied:
            Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/{world_group}/configs/server/config/paper-global.yml`
        otherwise:
            Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/defaultconfigs/config/paper-global.yml`

        Args:
            env (str): Environment name string
            world_group (Optional[str]): World Group name. Eg, 'creative', 'survival', 'gensokyo'

        Returns:
            Path: paper-global.yml path
        """
        base_path = (
            ServerPaths.get_config_path(env, world_group, ConfigType.SERVER)
            if world_group is not None
            else ServerPaths.get_env_default_configs_path(env) / "server"
        )

        return base_path / "config" / "paper-global.yml"
