from dataclasses import dataclass
from typing import Optional
import requests  # type: ignore
import urllib.request

from pprint import pformat

from src.common import server_paths
from src.common.types import ServerTypes
from src.common.environment import Env
from src.common.logger_setup import logger

MODRINTH_VERSION_URL_FMT = 'https://api.modrinth.com/v2/project/{project_id}/version?game_versions=["{mc_version}"]&loaders=["{loader}"]'

FABRICPROXY_LITE_PROJECT_ID = "8dI2tmqs"


@dataclass
class PluginModDefinition:
    """Represents a plugin or mod (paper, fabric, etc) definition."""

    project_id: str
    mod_mc_version: str

    _server_type: Optional[ServerTypes]
    _env: Optional[Env]

    def __init__(
        self,
        project_id: str,
        mod_mc_version: str,
        server_type: Optional[ServerTypes] = None,
        env: Optional[Env] = None,
    ):
        self.project_id = project_id
        self.mod_mc_version = mod_mc_version
        self._server_type = server_type
        self._env = env

        self.validate()

    def validate(self):
        """Validates the dataclass was instantiated with acceptable values..

        Raises:
            RuntimeError: If instantiated with neither `server_type` or `env`
            RuntimeError: If instantiated without a `project_id`
            RuntimeError: If instantiated without a `mod_mc_version`
        """
        if self.server_type is None and self.env is None:
            raise RuntimeError(
                "Got an invalid PluginModDefinition - both server_type and env were None! Must set one."
            )
        if self.project_id is None:
            raise RuntimeError(
                "Got an invalid PluginModDefinition - project_id was None! Must be a string of the project id."
            )
        if self.mod_mc_version is None:
            raise RuntimeError(
                "Got an invalid PluginModDefinition - mod_mc_version was None! Must be a string of the target mod version."
            )

    @property
    def server_type(self):
        """Returns the `server_type` this PluginModDefinition was instantiated with

        Returns:
            ServerTypes: The server type this PluginModDefinition is for.
        """
        if self._server_type:
            return self._server_type

        return self._env.cluster_vars.get(
            "MC_TYPE", "invalid-server-type-from-env"
        ).lower()

    @property
    def env(self):
        """Returns the `env` this PluginModDefinition was instantiated with

        Raises:
            RuntimeError: If this method is called but no `env` was supplied at instantiation.

        Returns:
            Env: The `env` that this PluginModDefinition should be installed to.
        """
        if self._env:
            return self._env

        raise RuntimeError(
            "Tried getting .env property of PluginModDefinition that did not have the env set!"
        )


def download_mod(pluginmod_definition: PluginModDefinition, env_name: str):
    """Downloads the plugin/mod defined by `pluginmod_definition` to `env_name`'s defaultmods directory

    Args:
        pluginmod_definition (PluginModDefinition): PluginMod to download
        env_name (str): Which env to download to

    Raises:
        RuntimeError: If the Modrinth response didn't include a `url` field in the `files` objects
        RuntimeError: If the Modrinth response didn't include a `filename` field in the `files` objects
    """

    mod_info = query_for_mod(pluginmod_definition)

    file_data = mod_info["files"][0]
    if "url" not in file_data:
        raise RuntimeError(
            "Got malformed response from Modrinth! Expected a 'url' field in the project download file data!"
        )
    if "filename" not in file_data:
        raise RuntimeError(
            "Got malformed response from Modrinth! Expected a 'filename' field in the project download file data!"
        )

    filename = file_data["filename"]
    mod_dl_url = file_data["url"]

    download_dest = server_paths.get_env_default_mods_path(env_name) / filename
    logger.info(f">> Downloading from '{mod_dl_url}' to '{download_dest}'!")
    urllib.request.urlretrieve(mod_dl_url, download_dest)


def query_for_mod(pluginmod_definition: PluginModDefinition):
    """Queries Modrinth API for a mod version that matches the `pluginmod_definition`

    Args:
        pluginmod_definition (PluginModDefinition): The plugin to query for

    Raises:
        RuntimeError: If Modrinth response did not return any projects for the `pluginmod_definition`
        RuntimeError: If Modrinth response did not include the `files` field.

    Returns:
        Dict: The Modrinth API response object per https://docs.modrinth.com/api/operations/getprojectversions/
    """
    fabric_proxy_url = MODRINTH_VERSION_URL_FMT.format(
        project_id=pluginmod_definition.project_id,
        mc_version=pluginmod_definition.mod_mc_version,
        loader=pluginmod_definition.server_type,
    )

    with requests.get(fabric_proxy_url) as r:
        resp = r.json()
        logger.info(fabric_proxy_url)
        logger.info(pformat(resp))
        if len(resp) == 0:
            raise RuntimeError(
                f"Modrinth API returned no valid downloads for project '{pluginmod_definition.project_id}'!"
            )

        project_version_data = resp[0]
        if (
            "files" not in project_version_data
            or len(project_version_data["files"]) == 0
        ):
            raise RuntimeError(
                "Got malformed response from Modrinth! Expected a 'files' field in the project version data!"
            )

        return project_version_data
