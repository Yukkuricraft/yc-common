#!/bin/env python3
import requests
import yaml  # type: ignore
import shutil

from pathlib import Path
import urllib.request

from src.common.helpers import log_exception, write_config
from src.common.config import ConfigNode, load_yaml_config
from src.common.config.config_finder import ConfigFinder
from src.common.config.yaml_config import YamlConfig
from src.common.constants import REPO_ROOT_PATH, VELOCITY_FORWARDING_SECRET_PATH
from src.common.types import DataDirType, ServerTypes
from src.common.paths import ServerPaths
from src.common.logger_setup import logger

from src.common.environment import Env

from src.generator.constants import PAPER_GLOBAL_TEMPLATE_PATH


class ServerTypeActions:
    server_root: Path

    def perform_only_once_actions(self, target_env: Env):
        """Performs ServerType based actions that are meant to be invoked only once, usually at env creation time.

        Args:
            target_env (Env): Env to run against
        """
        logger.info("Performing 'only once' server type actions")

        if target_env.server_type in ["FABRIC", "FORGE"]:
            self.write_fabric_proxy_files(target_env)
        elif target_env.server_type in ["PAPER", "BUKKIT"]:
            self.write_paper_bukkit_configs(target_env)
        else:
            logger.info(
                f"No special actions taken for server type: {target_env.server_type}"
            )

    def write_paper_bukkit_configs(self, target_env: Env):
        logger.info(f"Writing paper/bukkit configs for env: '{target_env.name}'")

        self.write_default_paper_global_yml_config(target_env)
        self.write_default_bukkit_yml_config(target_env)

    def write_default_paper_global_yml_config(self, target_env: Env):
        velocity_forwarding_secret = "CouldNotFindValidSecret?"
        curr_dir = Path(__file__).parent

        try:
            with open(VELOCITY_FORWARDING_SECRET_PATH, "r") as f:
                secret = f.read().strip()
                velocity_forwarding_secret = (
                    secret if len(secret) > 0 else velocity_forwarding_secret
                )
        except FileNotFoundError:
            log_exception(message=f"Could not load {VELOCITY_FORWARDING_SECRET_PATH}")

        # TODO: Need a cleaner way to handle different dir prefixes
        paper_global_yml_path = ServerPaths.get_paper_global_yml_path(target_env.name)
        if not paper_global_yml_path.exists():
            # TODO: ServerPaths? Relies on a non-common const though. Do we move them all to common?
            paper_global_tpl = load_yaml_config(
                curr_dir.parent / "generator" / PAPER_GLOBAL_TEMPLATE_PATH
            )
        else:
            paper_global_tpl = load_yaml_config(
                str(paper_global_yml_path), "/"
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

    def write_default_bukkit_yml_config(self, target_env: Env):
        """Writes the `bukkit.yml` file for a given target env

        Args:
            target_env (Env): Env to
        """

        # Because we don't actually dynamically inject any values into the template, don't do anything if file already exists.
        # At best it's a no op, at worst we overwrite changes.
        dest_bukkit_yml_path = ServerPaths.get_bukkit_yml_path(target_env.name)
        if not dest_bukkit_yml_path.exists():
            logger.info(f"Writing 'bukkit.yml' to 'defaultconfigs' for env: '{target_env.name}'")

            # TODO: ServerPaths? Relies on a non-common const though. Do we move them all to common?
            curr_dir = Path(__file__).parent
            template_path = curr_dir.parent / "generator" / "templates" / "bukkit.tpl.yml"

            shutil.copy(
                template_path,
                dest_bukkit_yml_path,
            )

    fabric_proxy_url_fmt = "https://api.modrinth.com/v2/project/8dI2tmqs/version?game_versions=[{mc_version}]&loaders=[{loader}]"
    def write_fabric_proxy_files(self, env: Env):
        """Downloads the appropriate Velocity/mcproxy related helper mods into the `server_only_mods` dir for `env`

        Args:
            env (Env): Env to target
        """

        fabric_proxy_url = self.fabric_proxy_url_fmt.format(
            mc_version=f'"{env.config.envvars.get("MC_VERSION", "no-mc-version-found")}"',
            loader=f'"{env.config.envvars.get("MC_TYPE", "invalid-server-type").lower()}"',
        )

        filename = None
        mod_dl_url = None
        with requests.get(fabric_proxy_url) as r:
            resp = r.json()
            if len(resp) == 0:
                raise RuntimeError("Modrinth API returned no valid downloads for the FabricProxy-Lite mod!")

            project_version_data = resp[0]
            if "files" not in project_version_data:
                raise RuntimeError("Got malformed response from Modrinth! Expected a 'files' field in the project version data!")

            file_data = project_version_data["files"]
            if "url" not in file_data:
                raise RuntimeError("Got malformed response from Modrinth! Expected a 'url' field in the project download file data!")
            if "filename" not in file_data:
                raise RuntimeError("Got malformed response from Modrinth! Expected a 'filename' field in the project download file data!")

            filename = file_data["filename"]
            mod_dl_url = file_data["url"]

        if mod_dl_url is None:
            raise Exception("Somehow got here with a None mod download url!")

        download_dest = ServerPaths.get()
        urllib.request.urlretrieve(mod_dl_url, filename)