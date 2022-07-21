from typing import Callable, Dict


# G w o s s
def serialize_tuple_out_as_dict(mapping: Dict[str, int]):
    def outer_wrap(func):
        def wrapper(*args, **kwargs):
            tuple_out = func(*args, **kwargs)

            rtn_dict = {}
            for field_name, tup_idx in mapping.items():
                rtn_dict[field_name] = tuple_out[tup_idx]

            return rtn_dict

        return wrapper

    return outer_wrap
