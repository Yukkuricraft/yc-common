from typing import TypeVar
from enum import Enum


class DataDirType(Enum):
    PLUGIN_CONFIGS = "plugin_config"
    MOD_CONFIGS = "mod_config"
    SERVER_CONFIGS = "server_config"

    LOG_FILES = "log_files"
    WORLD_FILES = "world_files"
    PLUGIN_FILES = "plugin_files"
    MOD_FILES = "mod_files"
    CLIENT_AND_SERVER_MOD_FILES = "client_and_server_mods"
    SERVER_ONLY_MOD_FILES = "server_only_mods"
    CRASH_REPORTS = "crash_reports"

    @staticmethod
    def from_str(label) -> "DataDirType":
        if label == "plugin_configs":
            return DataDirType.PLUGIN_CONFIGS
        elif label == "mod_configs":
            return DataDirType.MOD_CONFIGS
        elif label == "server_configs":
            return DataDirType.SERVER_CONFIGS
        elif label == "log_files":
            return DataDirType.LOG_FILES
        elif label == "world_files":
            return DataDirType.WORLD_FILES
        elif label == "plugin_files":
            return DataDirType.PLUGIN_FILES
        elif label == "mod_files":
            return DataDirType.MOD_FILES
        elif label == "client_and_server_mods":
            return DataDirType.CLIENT_AND_SERVER_MOD_FILES
        elif label == "server_only_mods":
            return DataDirType.SERVER_ONLY_MOD_FILES
        elif label == "crash_reports":
            return DataDirType.CRASH_REPORTS
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
