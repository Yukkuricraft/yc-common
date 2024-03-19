from pathlib import Path
from typing import Optional

from src.common.types import DataDirType
from src.common.constants import BASE_DATA_PATH, HOST_REPO_ROOT_PATH, REPO_ROOT_PATH, RESTIC_REPO_PATH


class ServerPaths:
    ##
    ## Repo based directory helpers
    ##

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

    @staticmethod
    def get_minecraft_db_env_file_path() -> Path:
        """Returns the path to the `minecraft_db.env` used to instantiate the Minecraft MySQL server with

        Returns:
            Path: Path to `minecraft_db.env`
        """
        return REPO_ROOT_PATH / "secrets" / "minecraft_db.env"

    @staticmethod
    def get_api_db_env_file_path() -> Path:
        """Returns the path to the `api_db.env` used to instantiate the API MySQL server with

        Returns:
            Path: Path to `api_db.env`
        """
        return REPO_ROOT_PATH / "secrets" / "api_db.env"

    @staticmethod
    def get_pg_pw_file_path() -> Path:
        """Returns the path to the `postgres_pw` file containing the default PG superuser password

        Returns:
            Path: Path to `postgres_pw`
        """
        return REPO_ROOT_PATH / "secrets" / "postgres_pw"

    @staticmethod
    def get_restic_password_file_path() -> Path:
        """Returns the path to the `restic.password` file containing the restic repo pass

        Returns:
            Path: Path to `restic.password`
        """
        return HOST_REPO_ROOT_PATH / "secrets" / "restic.password"

    @staticmethod
    def get_rcon_password_file_path() -> Path:
        """Returns the path to the `rcon.password` file containing the rcon repo pass

        Returns:
            Path: Path to `rcon.password`
        """
        return HOST_REPO_ROOT_PATH / "secrets" / "rcon.password"

    ##
    ## Base data path based directory helpers
    ##

    @staticmethod
    def get_env_data_path(env_str: str) -> Path:
        """Get the base data path for a given `env`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/`

        Args:
            env (env_str): Environment

        Returns:
            Path: Base data path for `env`
        """
        return BASE_DATA_PATH / "env" / env_str

    @staticmethod
    def get_mysql_env_data_path(env_str: str) -> Path:
        """Get the base mysql data path for a given `env`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/mysql`

        Args:
            env (env_str): Environment

        Returns:
            Path: Base data path for `env`
        """
        return ServerPaths.get_env_data_path(env_str) / "mysql"

    @staticmethod
    def get_pg_env_data_path(env_str: str) -> Path:
        """Get the base postgres data path for a given `env`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/pg`

        Args:
            env (env_str): Environment

        Returns:
            Path: Base data path for `env`
        """
        return ServerPaths.get_env_data_path(env_str) / "postgres"

    @staticmethod
    def get_mc_env_data_path(env_str: str) -> Path:
        """Get the base minecraft data path for a given `env`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/minecraft`

        Args:
            env (env_str): Environment

        Returns:
            Path: Base data path for `env`
        """
        return ServerPaths.get_env_data_path(env_str) / "minecraft"

    @staticmethod
    def get_env_default_configs_path(env_str: str) -> Path:
        """Get the default configs path for a given `env`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/minecraft/defaultconfigs`

        Args:
            env (env_str): Environment

        Returns:
            Path: Default configs path
        """
        return ServerPaths.get_mc_env_data_path(env_str) / "defaultconfigs"

    @staticmethod
    def get_env_and_world_group_path(env_str: str, world_group: str) -> Path:
        """Get the data path for a specific `env` and `world_group`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/minecraft/{world_group}`

        Args:
            env (env_str): Environment
            world_group (str): World Group name. Eg, 'creative', 'survival', 'gensokyo'

        Returns:
            Path: Data path for `env` and `world_group`
        """
        return ServerPaths.get_mc_env_data_path(env_str) / world_group

    @staticmethod
    def get_env_and_world_group_configs_path(env_str: str, world_group: str) -> Path:
        """Get the config data path for a specific `env` and `world_group`.

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/minecraft/{world_group}/configs`

        Args:
            env (env_str): Environment
            world_group (str): World Group name. Eg, 'creative', 'survival', 'gensokyo'

        Returns:
            Path: Config path
        """
        return (
            ServerPaths.get_env_and_world_group_path(env_str, world_group) / "configs"
        )

    DATA_DIR_TYPE_TO_PATH_MAPPING = {
        DataDirType.PLUGIN_CONFIGS: (
            lambda env_str, world_group: ServerPaths.get_env_and_world_group_configs_path(
                env_str, world_group
            )
            / "plugins"
        ),
        DataDirType.MOD_CONFIGS: (
            lambda env_str, world_group: ServerPaths.get_env_and_world_group_configs_path(
                env_str, world_group
            )
            / "mods"
        ),
        DataDirType.SERVER_CONFIGS: (
            lambda env_str, world_group: ServerPaths.get_env_and_world_group_configs_path(
                env_str, world_group
            )
            / "server"
        ),
        DataDirType.LOG_FILES: (
            lambda env_str, world_group: ServerPaths.get_env_and_world_group_path(
                env_str, world_group
            )
            / "logs"
        ),
        DataDirType.WORLD_FILES: (
            lambda env_str, world_group: ServerPaths.get_env_and_world_group_path(
                env_str, world_group
            )
            / "worlds"
        ),
        DataDirType.PLUGIN_FILES: (
            lambda env_str, world_group: ServerPaths.get_env_and_world_group_path(
                env_str, world_group
            )
            / "plugins"
        ),
        DataDirType.MOD_FILES: (
            lambda env_str, world_group: ServerPaths.get_env_and_world_group_path(
                env_str, world_group
            )
            / "mods"
        ),
        DataDirType.SERVER_ONLY_MOD_FILES: (
            lambda env_str, world_group: ServerPaths.get_env_and_world_group_path(
                env_str, world_group
            )
            / "server-only-mods"
        ),
        DataDirType.CLIENT_AND_SERVER_MOD_FILES: (
            lambda env_str, world_group: ServerPaths.get_env_and_world_group_path(
                env_str, world_group
            )
            / "client-and-server-mods"
        ),
        DataDirType.CRASH_REPORTS: (
            lambda env_str, world_group: ServerPaths.get_env_and_world_group_path(
                env_str, world_group
            )
            / "crash-reports"
        ),
    }

    @staticmethod
    def get_data_dir_path(
        env_str: str, world_group: str, data_dir_type: DataDirType
    ) -> Path:
        """Get the file path for a given `env`, `world_group`, and `data_file_type`.

        See `ServerPaths.DATA_DIR_TYPE_TO_PATH_MAPPING` for more details

        Args:
            env (env_str): Environment to get data files for
            world_group (str): World Group name. Eg, 'creative', 'survival', 'gensokyo'
            data_dir_type (DataDirType): Config type to return path for

        Returns:
            Path: Config path
        """

        if data_dir_type in ServerPaths.DATA_DIR_TYPE_TO_PATH_MAPPING:
            return ServerPaths.DATA_DIR_TYPE_TO_PATH_MAPPING[data_dir_type](
                env_str, world_group
            )
        else:
            raise RuntimeError(
                f"Got a data_dir_type we don't support? Got: '{data_dir_type}'"
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
        return (
            ServerPaths.get_generated_configs_path() / f"docker-compose-{env_str}.yml"
        )

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

        Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/minecraft/{world_group}/configs/server/server.properties`

        Args:
            env (env_str): Environment to get properties for
            world_group (str): World Group name. Eg, 'creative', 'survival', 'gensokyo'

        Returns:
            Path: Server.properties path
        """
        return (
            ServerPaths.get_data_dir_path(
                env_str, world_group, DataDirType.SERVER_CONFIGS
            )
            / "server.properties"
        )

    @staticmethod
    def get_paper_global_yml_path(
        env_str: str, world_group: Optional[str] = None
    ) -> Path:
        """Returns the `paper-global.yml` path for a given `env` and optional `world_group`

        If `world_group` supplied:
            Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/minecraft/{world_group}/configs/server/config/paper-global.yml`
        otherwise:
            Equivalent to `{constants.BASE_DATA_PATH}/env/{env}/minecraft/defaultconfigs/config/paper-global.yml`

        Args:
            env (env_str): Environment to get yml for
            world_group (Optional[str]): World Group name. Eg, 'creative', 'survival', 'gensokyo'

        Returns:
            Path: paper-global.yml path
        """
        base_path = (
            ServerPaths.get_data_dir_path(
                env_str, world_group, DataDirType.SERVER_CONFIGS
            )
            if world_group is not None
            else ServerPaths.get_env_default_configs_path(env_str) / "server"
        )

        return base_path / "config" / "paper-global.yml"
