#!/usr/bin/env python3

from pprint import pformat
from typing import List, Tuple, Dict


class ConfigNode:
    data: Dict

    def __getattr__(self, name):
        rtn = self.data[name]
        return rtn

    def __getitem__(self, name):
        return self.data[name]

    def __contains__(self, item):
        return item in self.data

    def __str__(self):
        lines = [
            "",
        ]
        for key, val in self.data.items():
            if type(val) in [dict, list]:
                val_str = pformat(val)
            else:
                val_str = val
            lines += "{}: {}".format(key, val_str).split("\n")
        return "\n    ".join(lines)

    def __repr__(self):
        return self.__str__()

    def listnodes(self) -> List[str]:
        return list(self.data.keys())

    def get_or_default(self, name, default=None):
        if name not in self.data:
            return default
        return self.__getitem__(name)

    def items(
        self,
    ) -> List[Tuple[str,]]:
        return list(self.data.items())  # type: ignore

    def __init__(self, data: Dict):
        self.data = {}

        for k, v in data.items():
            if type(v) in [int, float, str, bool, list]:
                self.data[k] = v
            elif v is not None:
                self.data[k] = ConfigNode(dict(v))
            else:
                self.data[k] = None

    def as_dict(self):
        rtn_dict = {}

        for key, value in self.data.items():
            if issubclass(type(value), ConfigNode):
                rtn_dict[key] = value.as_dict()
            else:
                rtn_dict[key] = value

        return rtn_dict
