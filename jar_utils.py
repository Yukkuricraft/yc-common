import zipfile
import yaml
import json
from pathlib import Path


class BaseHandler:
    data: dict

    def get_name(self) -> str:
        return self.data.get("name", "COULDNOTFINDPLUGINMODNAME")

    def get_version(self) -> str:
        return self.data.get("version", "COULDNOTFINDPLUGINMODVERSION")


class JsonHandler(BaseHandler):
    def __init__(self, file: Path):
        with file.open("r") as f:
            self.data = json.loads(f.read())


class YamlHandler(BaseHandler):
    def __init__(self, file: Path):
        with file.open("r") as f:
            self.data = yaml.load(f.read())


PLUGINMOD_INFO_FILE = {
    "plugin.yml": YamlHandler,
    "fabric.mod.json": JsonHandler,
}


def get_pluginmod_info_handler(file: Path) -> BaseHandler:
    """Returns a subclass of BaseHandler that implements pluginmod info helpers.

    Assumes the necessary information file (Eg, `plugin.yml`, `fabric.mod.json`) exists on the root level of the jar.
    """
    jar = zipfile.Path(file)
    for file in jar.iterdir():
        if file.is_dir():
            continue

        if file.name not in PLUGINMOD_INFO_FILE:
            continue

        return PLUGINMOD_INFO_FILE[file.name](file)

    raise RuntimeError(f"Could not find a valid pluginmod info file in '{file}'!")


def get_pluginmod_name(file: Path):
    return get_pluginmod_info_handler(file).get_name()


def get_pluginmod_version(file: Path):
    return get_pluginmod_info_handler(file).get_version()
