import shutil

import requests

from pathlib import Path
from typing import Optional

from src.common.helpers import log_exception, write_config
from src.common.config import load_yaml_config
from src.common.config.yaml_config import YamlConfig
from src.common.constants import VELOCITY_FORWARDING_SECRET_PATH
from src.common.logger_setup import logger
from src.common import jar_utils, modrinth, server_paths

from src.common.environment import Env

from src.generator.constants import PAPER_GLOBAL_TEMPLATE_PATH


def perform_only_once_actions(target_env: Env):
    """Performs ServerType based actions that are meant to be invoked only once, usually at env creation time.

    Args:
        target_env (Env): Env to run against
    """
    logger.info("Performing 'only once' server type actions")

    if target_env.server_type in ["PAPER", "BUKKIT"]:
        write_paper_bukkit_configs(target_env)
    else:
        logger.info(
            f"No special actions taken for server type: {target_env.server_type}"
        )


def write_paper_bukkit_configs(target_env: Env):
    logger.info(f"Writing paper/bukkit configs for env: '{target_env.name}'")

    if target_env.server_version >= "1.19":
        # Versions before 1.19 did not have a paper-global.yml
        write_default_paper_global_yml_config(target_env)

    write_default_bukkit_yml_config(target_env)


MINIMUM_VERSION_FOR_PAPER_GLOBAL = "1.19"
default_configs_repo_url_fmt = "https://raw.githubusercontent.com/dayyeeet/minecraft-default-configs/refs/heads/main/{server_version}"
default_paper_global_url_fmt = f"{default_configs_repo_url_fmt}/paper-global.yml"
default_paper_world_defaults_url_fmt = (
    f"{default_configs_repo_url_fmt}/paper-world-defaults.yml"
)


def get_paper_global_template_content(target_env: Env):
    """Gets the content of the default or template paper-global.yml file

    Args:
        target_env (Env): The env to create paper-global.yml for.

    Raises:
        RuntimeError: If supplied `target_env`'s server version is too low
    """
    if target_env.server_version < MINIMUM_VERSION_FOR_PAPER_GLOBAL:
        raise RuntimeError(
            f"Tried getting default paper-global.yml file for a version that doesn't have that file! Got '{target_env.server_version}'"
        )

    default_paper_global_url = default_paper_global_url_fmt.format(
        server_version=target_env.server_version
    )
    with requests.get(default_paper_global_url) as r:
        return r.text


def write_default_paper_global_yml_config(target_env: Env):
    """Writes the `paper-global.yml` file for a given target env

    Args:
        target_env (Env): The env to write `paper-global.yml` into.
    """
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

    paper_global_tpl = YamlConfig(get_paper_global_template_content(target_env))
    paper_global_config = paper_global_tpl.as_dict()
    paper_global_config["proxies"]["velocity"]["secret"] = velocity_forwarding_secret
    paper_global_config["proxies"]["velocity"]["enabled"] = True
    paper_global_config["proxies"]["velocity"][
        "online-mode"
    ] = False  # We use Velocity Modern Forwarding

    paper_global_yml_path = server_paths.get_paper_global_yml_path(target_env.name)
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


def write_default_bukkit_yml_config(target_env: Env):
    """Writes the `bukkit.yml` file for a given target env

    Args:
        target_env (Env): The env to write `bukkit.yml` into.
    """

    # Because we don't actually dynamically inject any values into the template, don't do anything if file already exists.
    # At best it's a no op, at worst we overwrite changes.
    dest_bukkit_yml_path = server_paths.get_bukkit_yml_path(target_env.name)
    if not dest_bukkit_yml_path.exists():
        logger.info(
            f"Writing 'bukkit.yml' to 'defaultconfigs' for env: '{target_env.name}'"
        )

        # TODO: server_paths? Relies on a non-common const though. Do we move them all to common?
        curr_dir = Path(__file__).parent
        template_path = curr_dir.parent / "generator" / "templates" / "bukkit.tpl.yml"

        shutil.copy(
            template_path,
            dest_bukkit_yml_path,
        )


def write_fabric_proxy_files(env: Env):
    """Downloads the appropriate Velocity/mcproxy related helper mods into the `server_only_mods` dir for `env`

    Args:
        env (Env): Env to target
    """

    fabric_proxy_version = env.cluster_vars.get("FABRIC_PROXY_VERSION", None)
    if not fabric_proxy_version:
        fabric_proxy_version = env.cluster_vars.get("MC_VERSION", "no-mc-version-found")

    jar_path = get_proxy_jar_path(env)
    if not jar_path:
        logger.info("Could not find an existing FabricProxy-Lite. Downloading now.")
        download_fabric_proxy_files(env, fabric_proxy_version)
    elif not is_proxy_jar_correct_version(jar_path, env, fabric_proxy_version):
        logger.info(
            "Found an existing FabricProxy-Lite with incorrect version. Deleting and redownloading correct version."
        )
        jar_path.unlink()
        download_fabric_proxy_files(env, fabric_proxy_version)
    else:
        logger.info("Found an existing FabricProxy-Lite with correct version.")


def get_proxy_jar_path(env: Env) -> Optional[Path]:
    """Check if there already exists a fabric proxy file.

    Args:
        env (Env): Env to check

    Returns:
        Path: If exists, returns a Path object to the jar
              Else, returns None
    """

    proxy_file_path = server_paths.get_env_default_mods_path(env.name)
    for file in proxy_file_path.iterdir():
        if file.suffix != ".jar":
            continue
        if jar_utils.get_pluginmod_name(file) == "FabricProxy Lite":
            return file
    return None


def is_proxy_jar_correct_version(
    jar_path: Path, env: Env, fabric_proxy_version: str
) -> bool:
    """Checks if the existing Fabric Proxy jar version in `env` matches the expected `fabric_proxy_version`.

    Args:
        jar_path (Path): Path to the FabricProxy jar
        env (Env): The env this is in
        fabric_proxy_version (str): The desired version of the Fabric Proxy

    Returns:
        bool: True if the existing jar version matches `fabric_proxy_version`. False otherwise.
    """
    mod_info = modrinth.query_for_mod(
        modrinth.PluginModDefinition(
            modrinth.FABRICPROXY_LITE_PROJECT_ID,
            fabric_proxy_version,
            env=env,
        )
    )

    expected_version = mod_info["name"]
    current_version = jar_utils.get_pluginmod_version(jar_path)

    return expected_version == current_version


def download_fabric_proxy_files(env: Env, fabric_proxy_version: str):
    """Wrapper around `modrinth.download_mod()` to download the Fabric proxy mod

    Args:
        env (Env): Env to install the mod into
        fabric_proxy_version (str): The Fabric Proxy version to download. Should match a version listed on the Fabric Proxy modrinth page.
    """
    modrinth.download_mod(
        modrinth.PluginModDefinition(
            modrinth.FABRICPROXY_LITE_PROJECT_ID,
            fabric_proxy_version,
            env=env,
        ),
        env.name,
    )


def download_modrinth_pluginmods() -> None:
    pass
