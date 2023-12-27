from typing import TypeVar
from enum import Enum

class ConfigType(Enum):
    PLUGIN = 'plugin'
    MOD = 'mod'
    SERVER = 'server'

    # Because luckperms is weird and puts half of its generated files in /data/mods instead of /data/configs :-/
    MOD_FILES = 'modfiles'

    @staticmethod
    def from_str(label) -> 'ConfigType':
        if label == 'plugin':
            return ConfigType.PLUGIN
        elif label == 'mod':
            return ConfigType.MOD
        elif label == 'modfiles':
            return ConfigType.MOD_FILES
        elif label == 'server':
            return ConfigType.SERVER
        else:
            raise NotImplementedError

class KnownServerTypes(Enum):
    FABRIC = "FABRIC"
    FORGE = "FORGE"
    PAPER = "PAPER"
    BUKKIT = "BUKKIT"
    CUSTOM = "CUSTOM"

    @staticmethod
    def from_str(label) -> 'KnownServerTypes':
        if label == 'plugin':
            return ConfigType.PLUGIN
        elif label == 'mod':
            return ConfigType.MOD
        elif label == 'modfiles':
            return ConfigType.MOD_FILES
        elif label == 'server':
            return ConfigType.SERVER
        else:
            raise NotImplementedError

ServerTypes = TypeVar('ServerTypes', KnownServerTypes, str)