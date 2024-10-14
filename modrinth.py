import requests  # type: ignore
import urllib.request

from pprint import pformat

from src.common import server_paths
from src.common.environment import Env
from src.common.logger_setup import logger

MODRINTH_VERSION_URL_FMT = 'https://api.modrinth.com/v2/project/{project_id}/version?game_versions=["{mc_version}"]&loaders=["{loader}"]'

FABRICPROXY_LITE_PROJECT_ID = "8dI2tmqs"


def download_mod(project_id: str, mod_mc_version: str, env: Env):
    mod_info = query_for_mod(
        project_id=project_id,
        mc_version=mod_mc_version,
        loader=f'"{env.cluster_vars.get("MC_TYPE", "invalid-server-type").lower()}"',
    )

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

    if mod_dl_url is None:
        raise Exception("Somehow got here with a None mod download url!")

    download_dest = server_paths.get_env_default_mods_path(env.name) / filename
    logger.info(f">> Downloading from '{mod_dl_url}' to '{download_dest}'!")
    urllib.request.urlretrieve(mod_dl_url, download_dest)


def query_for_mod(project_id: str, mc_version: str, loader: str):
    fabric_proxy_url = MODRINTH_VERSION_URL_FMT.format(
        project_id=project_id,
        mc_version=mc_version,
        loader=loader,
    )

    with requests.get(fabric_proxy_url) as r:
        resp = r.json()
        logger.info(fabric_proxy_url)
        logger.info(pformat(resp))
        if len(resp) == 0:
            raise RuntimeError(
                f"Modrinth API returned no valid downloads for project '{project_id}'!"
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
