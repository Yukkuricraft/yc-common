#!/bin/env python3
import yaml  # type: ignore
import shutil

from pathlib import Path

from src.common.helpers import log_exception, write_config
from src.common.config import ConfigNode, load_yaml_config
from src.common.config.config_finder import ConfigFinder
from src.common.config.yaml_config import YamlConfig
from src.common.constants import VELOCITY_FORWARDING_SECRET_PATH
from src.common.types import DataFileType, ServerTypes
from src.common.paths import ServerPaths
from src.common.logger_setup import logger

from src.common.environment import Env

from src.generator.constants import PAPER_GLOBAL_TEMPLATE_PATH


class ServerTypeActions:
    server_root: Path

    def run(self, target_env: Env):
        logger.info("Doing server type specific stuff?")

        if target_env.server_type in ["FABRIC", "FORGE"]:
            self.merge_fabric_forge_prereq_mods(target_env)
        elif target_env.server_type in ["PAPER", "BUKKIT"]:
            self.write_paper_bukkit_configs(target_env)
        else:
            logger.info(
                f"No special actions taken for serer type: {target_env.server_type}"
            )

    def write_paper_bukkit_configs(self, target_env: Env):
        logger.info(f"Writing paper/bukkit configs for env: '{target_env.name}'")
        paper_global_yml_path = ServerPaths.get_paper_global_yml_path(target_env.name)
        velocity_forwarding_secret = "CouldNotFindValidSecret?"
        curr_dir = Path(__file__).parent
        velocity_secret_path = ConfigFinder(
            str(VELOCITY_FORWARDING_SECRET_PATH), curr_dir
        ).config_path

        try:
            with open(velocity_secret_path, "r") as f:
                secret = f.read().strip()
                velocity_forwarding_secret = (
                    secret if len(secret) > 0 else velocity_forwarding_secret
                )
        except FileNotFoundError:
            log_exception(
                message=f"Could not load {velocity_secret_path}"
            )

        # TODO: Need a cleaner way to handle different dir prefixes
        paper_global_tpl = load_yaml_config(
            f"generator/{PAPER_GLOBAL_TEMPLATE_PATH}", curr_dir
        )

        paper_global_config = paper_global_tpl.as_dict()
        paper_global_config["proxies"]["velocity"][
            "secret"
        ] = velocity_forwarding_secret

        write_config(
            paper_global_yml_path,
            paper_global_config,
            (
                "#\n"
                "# This file is largely unmodified from paper defaults except for proxies.velocity values.\n"
                "# Particularly, proxies.velocity.secret is set to the value in our velocity secrets file."
                "#\n\n"
            ),
            YamlConfig.write_cb,
        )

    def merge_fabric_forge_prereq_mods(self, env: Env):
        """Copies mods from the "server only" and "client + server" mods folders into the final "mods" folder.

        The user should place their mods in the "server only" and "client + server" mods folders.
        The "mods" folder is cleared and recreated on each restart.

        Args:
            env (Env): Env to run for.
        """
        logger.info(f"Merging fabric/forge prereq mods for env '{env.name}'")
        for world in env.world_groups:
            server_mods_path = ServerPaths.get_data_files_path(
                env.name, world, DataFileType.SERVER_ONLY_MOD_FILES
            )
            server_client_mods_path = ServerPaths.get_data_files_path(
                env.name, world, DataFileType.CLIENT_AND_SERVER_MOD_FILES
            )
            mods_path = ServerPaths.get_data_files_path(
                env.name, world, DataFileType.MOD_FILES
            )

            # Clear out and recreate mods directory
            if mods_path.exists():
                shutil.rmtree(mods_path)
                mods_path.mkdir(parents=True)

            for mods_to_merge_path in [server_mods_path, server_client_mods_path]:
                if mods_to_merge_path.exists():
                    logger.info(
                        f"[{env.name}][{world}] Copying '{mods_to_merge_path}' => '{mods_path}'"
                    )
                    shutil.copytree(
                        mods_to_merge_path,
                        mods_path,
                        dirs_exist_ok=True,
                        symlinks=True,  # Should we literally ever encounter symlinks lol
                    )
                else:
                    logger.warning(
                        f"Tried copying files from '{mods_to_merge_path}' but path did not exist!"
                    )
