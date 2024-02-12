from typing import TypeVar
from enum import Enum


class DataFileType(Enum):
    PLUGIN_CONFIGS = "plugin_config"
    MOD_CONFIGS = "mod_config"
    SERVER_CONFIGS = "server_config"

    LOG_FILES = "log_files"
    WORLD_FILES = "world_files"
    PLUGIN_FILES = "plugin_files"
    MOD_FILES = "mod_files"
    CLIENT_AND_SERVER_MOD_FILES = "client_and_server_mods"
    SERVER_ONLY_MOD_FILES = "server_only_mods"

    @staticmethod
    def from_str(label) -> "DataFileType":
        if label == "plugin_configs":
            return DataFileType.PLUGIN_CONFIGS
        elif label == "mod_configs":
            return DataFileType.MOD_CONFIGS
        elif label == "server_configs":
            return DataFileType.SERVER_CONFIGS
        elif label == "log_files":
            return DataFileType.LOG_FILES
        elif label == "world_files":
            return DataFileType.WORLD_FILES
        elif label == "plugin_files":
            return DataFileType.PLUGIN_FILES
        elif label == "mod_files":
            return DataFileType.MOD_FILES
        elif label == "client_and_server_mods":
            return DataFileType.CLIENT_AND_SERVER_MOD_FILES
        elif label == "server_only_mods":
            return DataFileType.SERVER_ONLY_MOD_FILES

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
