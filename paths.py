from pathlib import Path
from typing import Optional

from src.common.types import DataFileType
from src.common.constants import BASE_DATA_PATH, REPO_ROOT_PATH


class ServerPaths:

    ## Repo based directory helpers

    @staticmethod
    def get_generated_configs_path() -> Path:
        """Get the path we dump all env-based generated files

        Equivalent to `{constants.REPO_ROOT_PATH}/gen`

        Think files like velocity configs, env files, docker compose files

        Returns:
            Path: Generated files path
        """
        return REPO_ROOT_PATH / "gen"

    @staticmethod
    def get_env_toml_config_dir_path() -> Path:
        """Get the path we expect the env toml configs to be in

        Equivalent to `{constants.REPO_ROOT_PATH}/env`

        Returns:
            Path: Dir path where we keep our env tomls
        """
        return REPO_ROOT_PATH / "env"

    ## Base data path based directory helpers

    @staticmethod
    def get_env_data_path(env_str: str) -> Path:
        """Get the base data path for a given `env`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}`

        Args:
            env (env_str): Environment

        Returns:
            Path: Base data path for `env`
        """
        return BASE_DATA_PATH / "env" / env_str

    @staticmethod
    def get_env_default_configs_path(env_str: str) -> Path:
        """Get the default configs path for a given `env`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/defaultconfigs`

        Args:
            env (env_str): Environment

        Returns:
            Path: Default configs path
        """
        return ServerPaths.get_env_data_path(env_str) / "defaultconfigs"

    @staticmethod
    def get_env_and_world_group_path(env_str: str, world_group: str) -> Path:
        """Get the data path for a specific `env` and `world_group`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/{world_group}`

        Args:
            env (env_str): Environment
            world_group (str): World Group name. Eg, 'creative', 'survival', 'gensokyo'

        Returns:
            Path: Data path for `env` and `world_group`
        """
        return BASE_DATA_PATH / "env" / env_str / world_group

    @staticmethod
    def get_env_and_world_group_configs_path(env_str: str, world_group: str) -> Path:
        """Get the config data path for a specific `env` and `world_group`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/{world_group}/configs`

        Args:
            env (env_str): Environment
            world_group (str): World Group name. Eg, 'creative', 'survival', 'gensokyo'

        Returns:
            Path: Config path
        """
        return ServerPaths.get_env_and_world_group_path(env_str, world_group) / "configs"

    SERVER_ONLY_MODS_FILE_DIR = "server_only_mods"
    CLIENT_AND_SERVER_MODS_FILE_DIR = "client_and_server_mods"
    MODS_FILE_DIR = "mods"
    MODS_CONFIG_DIR = "mods"
    PLUGINS_CONFIG_DIR = "plugins"
    WORLDS_CONFIG_DIR = "server"

    @staticmethod
    def get_data_files_path(env_str: str, world_group: str, data_file_type: DataFileType) -> Path:
        """Get the file path for a given `env`, `world_group`, and `data_file_type`.

        For configs
        - Normally:
            - Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/{world_group}/configs/{data_file_type_dirname}`
        - Except for `DataFileType.MOD_FILES` because lol LuckPerms and generating files in the mod files directory:
            - Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/{world_group}/mods`

        For mods
        - We have three directories
            - Server only mods
            - Server + client mods
            - "Mods folder"
        - Place mods into first two directories. Third directory is cleared on each startup and the other two folders merged.
            - This is to allow independently updating each folder without needing to remove old versions of mods.

        Args:
            env (env_str): Environment to get data files for
            world_group (str): World Group name. Eg, 'creative', 'survival', 'gensokyo'
            data_file_type (DataFileType): Config type to return path for

        Returns:
            Path: Config path
        """

        if data_file_type == DataFileType.MOD_FILES:
            return (
                ServerPaths.get_env_and_world_group_path(env_str, world_group)
                / ServerPaths.MODS_FILE_DIR
            )
        elif data_file_type == DataFileType.SERVER_ONLY_MOD_FILES:
            return (
                ServerPaths.get_env_and_world_group_path(env_str, world_group)
                / ServerPaths.SERVER_ONLY_MODS_FILE_DIR
            )
        elif data_file_type == DataFileType.CLIENT_AND_SERVER_MOD_FILES:
            return (
                ServerPaths.get_env_and_world_group_path(env_str, world_group)
                / ServerPaths.CLIENT_AND_SERVER_MODS_FILE_DIR
            )
        elif data_file_type == DataFileType.MOD_CONFIGS:
            return (
                ServerPaths.get_env_and_world_group_configs_path(env_str, world_group)
                / ServerPaths.MODS_CONFIG_DIR
            )
        elif data_file_type == DataFileType.PLUGIN_CONFIGS:
            return (
                ServerPaths.get_env_and_world_group_configs_path(env_str, world_group)
                / ServerPaths.PLUGINS_CONFIG_DIR
            )
        elif data_file_type == DataFileType.SERVER_CONFIGS:
            return (
                ServerPaths.get_env_and_world_group_configs_path(env_str, world_group)
                / ServerPaths.WORLDS_CONFIG_DIR
            )


    ## Repo based specific filepath helpers

    @staticmethod
    def get_env_toml_config_path(env_str: str) -> Path:
        """Get the toml config path for `env`.

        Equivalent to `{constants.REPO_ROOT_PATH}/env/{env}.toml`

        Args:
            env (env_str): Environment to get path for

        Returns:
            Path: Env toml config path
        """
        return ServerPaths.get_env_toml_config_dir_path() / f"{env_str}.toml"

    @staticmethod
    def get_generated_docker_compose_path(env_str: str) -> Path:
        """Returns the `docker-compose-{env}.yml` path for a given `env`.

        Equivalent to `{constants.REPO_ROOT_PATH}/gen/docker-compose-{env}.yml`

        Args:
            env (env_str): Environment to get path for

        Returns:
            Path: Generated `docker-compose-{env}.yml` path
        """
        return ServerPaths.get_generated_configs_path() / f"docker-compose-{env_str}.yml"

    @staticmethod
    def get_generated_env_file_path(env_str: str) -> Path:
        """Returns the `{env}.env` path for a given `env`.

        Equivalent to `{constants.REPO_ROOT_PATH}/gen/{env}.env`

        Args:
            env (env_str): Environment to get path for

        Returns:
            Path: Generated `{env}.env` path
        """
        return ServerPaths.get_generated_configs_path() / f"{env_str}.env"

    @staticmethod
    def get_generated_velocity_config_path(env_str: str) -> Path:
        """Returns the `velocity-{env}.toml` path for a given `env`.

        Equivalent to `{constants.REPO_ROOT_PATH}/gen/velocity-{env}.toml`

        Args:
            env (env_str): Environment to get config for

        Returns:
            Path: Generated `velocity-{env}.toml` path
        """
        return ServerPaths.get_generated_configs_path() / f"velocity-{env_str}.toml"

    ## Base data path based specific filepath helpers

    @staticmethod
    def get_server_properties_path(env_str: str, world_group: str) -> Path:
        """Returns the `server.properties` path for a given `env` and `world_group`

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/{world_group}/configs/server/server.properties`

        Args:
            env (env_str): Environment to get properties for
            world_group (str): World Group name. Eg, 'creative', 'survival', 'gensokyo'

        Returns:
            Path: Server.properties path
        """
        return (
            ServerPaths.get_data_files_path(env_str, world_group, DataFileType.SERVER_CONFIGS)
            / "server.properties"
        )

    @staticmethod
    def get_paper_global_yml_path(env_str: str, world_group: Optional[str] = None) -> Path:
        """Returns the `paper-global.yml` path for a given `env` and optional `world_group`

        If `world_group` supplied:
            Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/{world_group}/configs/server/config/paper-global.yml`
        otherwise:
            Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/defaultconfigs/config/paper-global.yml`

        Args:
            env (env_str): Environment to get yml for
            world_group (Optional[str]): World Group name. Eg, 'creative', 'survival', 'gensokyo'

        Returns:
            Path: paper-global.yml path
        """
        base_path = (
            ServerPaths.get_data_files_path(env_str, world_group, DataFileType.SERVER_CONFIGS)
            if world_group is not None
            else ServerPaths.get_env_default_configs_path(env_str) / "server"
        )

        return base_path / "config" / "paper-global.yml"