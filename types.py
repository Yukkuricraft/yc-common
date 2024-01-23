from typing import TypeVar
from enum import Enum


class DataFileType(Enum):
    PLUGIN_CONFIGS = "plugin"
    MOD_CONFIGS = "mod"
    SERVER_CONFIGS = "server"

    MOD_FILES = "modfiles"
    SERVER_ONLY_MOD_FILES = "server_only_mods"

    @staticmethod
    def from_str(label) -> "DataFileType":
        if label == "plugin":
            return DataFileType.PLUGIN_CONFIGS
        elif label == "mod":
            return DataFileType.MOD_CONFIGS
        elif label == "modfiles":
            return DataFileType.MOD_FILES
        elif label == "server_only_mods":
            return DataFileType.SERVER_ONLY_MOD_FILES
        elif label == "server":
            return DataFileType.SERVER_CONFIGS
        else:
            raise NotImplementedError


class KnownServerTypes(Enum):
    FABRIC = "FABRIC"
    FORGE = "FORGE"
    PAPER = "PAPER"
    BUKKIT = "BUKKIT"
    CUSTOM = "CUSTOM"

    @staticmethod
    def from_str(label) -> "KnownServerTypes":
        if label == "plugin":
            return DataFileType.PLUGIN_CONFIGS
        elif label == "mod":
            return DataFileType.MOD_CONFIGS
        elif label == "modfiles":
            return DataFileType.MOD_FILES
        elif label == "server":
            return DataFileType.SERVER_CONFIGS
        else:
            raise NotImplementedError


ServerTypes = TypeVar("ServerTypes", KnownServerTypes, str)
