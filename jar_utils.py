import zipfile
import yaml  # type: ignore
import json
from pathlib import Path


class BaseHandler:
    data: dict

    def get_name(self) -> str:
        return self.data.get("name", "COULDNOTFINDPLUGINMODNAME")

    def get_version(self) -> str:
        return self.data.get("version", "COULDNOTFINDPLUGINMODVERSION")


class JsonHandler(BaseHandler):
    def __init__(self, file: zipfile.Path):
        with file.open("r") as f:
            self.data = json.loads(f.read())


class YamlHandler(BaseHandler):
    def __init__(self, file: zipfile.Path):
        with file.open("r") as f:
            self.data = yaml.load(f.read())


PLUGINMOD_INFO_FILE = {
    "plugin.yml": YamlHandler,
    "fabric.mod.json": JsonHandler,
}


def get_pluginmod_info_handler(jar_path: Path) -> BaseHandler:
    """Returns a subclass of BaseHandler that implements pluginmod info helpers.

    Assumes the necessary information file (Eg, `plugin.yml`, `fabric.mod.json`) exists on the root level of the jar.

    Args:
        jar_path (Path): Path to the jar we're inspecting

    Raises:
        RuntimeError: If we could not find a valid pluginmod info file in jar_path

    Returns:
        BaseHandler: Either a JsonHandler or YamlHandler instance depending on if we detected a `plugin.yml` or `fabric.mod.json` inside the jar.
    """

    jar = zipfile.Path(jar_path)
    for file in jar.iterdir():
        if file.is_dir():
            continue

        if file.name not in PLUGINMOD_INFO_FILE:
            continue

        return PLUGINMOD_INFO_FILE[file.name](file)

    raise RuntimeError(f"Could not find a valid pluginmod info file in '{jar_path}'!")


def get_pluginmod_name(jar_path: Path):
    """Given a jar, inspects its contents to find the pluginmod name.

    Can handle Paper and Fabric mods

    Args:
        file (Path): Path to the jar

    Returns:
        str: Name of the pluginmod defined within the jar
    """
    return get_pluginmod_info_handler(jar_path).get_name()


def get_pluginmod_version(jar_path: Path):
    """Given a jar, inspects its contents to find the pluginmod version.

    Can handle Paper and Fabric mods

    Args:
        file (Path): Path to the jar

    Returns:
        str: Version defined in the pluginmod jar
    """
    return get_pluginmod_info_handler(jar_path).get_version()
