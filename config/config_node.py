#!/usr/bin/env python3

from pprint import pformat
from typing import TextIO, List, Tuple, Dict


class ConfigNode:
    data: Dict

    # TODO: Handle hyphenated dict keys? Should we auto coalesce?

    def __getattr__(self, name):
        hyphenated_name = name.replace("_", "-")

        if name in self.data:
            return self.data[name]
        elif hyphenated_name in self.data:
            return self.data[hyphenated_name]
        else:
            return ConfigNode({})

    def __getitem__(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return ConfigNode({})

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

    def get(self, name, default=None):
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

    @staticmethod
    def write_cb(f: TextIO, config: Dict):
        raise NotImplementedError(
            "Called write_cb on a subclass that hasn't overwritten it!"
        )
