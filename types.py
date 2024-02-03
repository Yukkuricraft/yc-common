from typing import TypeVar
from enum import Enum


class DataFileType(Enum):
    PLUGIN_CONFIGS = "plugin"
    MOD_CONFIGS = "mod"
    SERVER_CONFIGS = "server"

    MOD_FILES = "modfiles"
    CLIENT_AND_SERVER_MOD_FILES = "client_and_server_mods"
    SERVER_ONLY_MOD_FILES = "server_only_mods"

    @staticmethod
    def from_str(label) -> "DataFileType":
        if label == "plugin":
            return DataFileType.PLUGIN_CONFIGS
        elif label == "mod":
            return DataFileType.MOD_CONFIGS
        elif label == "modfiles":
            return DataFileType.MOD_FILES
        elif label == "client_and_server_mods":
            return DataFileType.CLIENT_AND_SERVER_MOD_FILES
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

    @staticmethod
    def from_str(label) -> "KnownServerTypes":
        if label == "FABRIC":
            return KnownServerTypes.FABRIC
        elif label == "FORGE":
            return KnownServerTypes.FORGE
        elif label == "PAPER":
            return KnownServerTypes.PAPER
        elif label == "BUKKIT":
            return KnownServerTypes.BUKKIT
        else:
            raise NotImplementedError


ServerTypes = TypeVar("ServerTypes", KnownServerTypes, str)
