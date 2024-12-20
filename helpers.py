import traceback
import os

from datetime import datetime, timezone
from typing import Optional, Dict, Callable, Any
from pprint import pformat
from pathlib import Path

from src.common.constants import DEFAULT_CHMOD_MODE
from src.common.logger_setup import logger


def get_now_dt() -> datetime:
    return datetime.now(timezone.utc)


def write_config(
    config_path: Path,
    config: Dict,
    write_cb: Callable,
    header: str = "",
):
    """Writes config to path with optional header and custom write cb

    Also applies `constants.DEFAULT_CHMOD_MODE`

    Args:
        config_path (Path): Path
        config (Dict): Config represented as a dict
        header (str, optional): Optional header. Defaults to "".
        write_cb (Callable, optional): Defaults to a `toml_w.dump()`.
    """

    if not config_path.parent.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "wb") as f:
        f.write(header.encode("utf8"))
        write_cb(f, config)
    os.chmod(config_path, DEFAULT_CHMOD_MODE)


def log_exception(
    message: Optional[str] = None,
    data: Optional[Any] = None,
    exception: Optional[Exception] = None,
):
    """Logging wrapper to be called inside `except:` blocks

    Allows logging of additional info like custom message and arbitrary data

    Args:
        message (Optional[str]): Custom error message. Defults to None
        data (Optional[Any]): Arbitrary data related to the exception to log. Defaults to None.
        exception (Optional[Exception]): If provided, we will use this exception object with `traceback`. Otherwise we use the last raised exception.
    """
    tb = None
    if exception is None:
        tb = traceback.format_exc()
    else:
        tb = "".join(
            traceback.format_exception(
                type(exception), exception, exception.__traceback__
            )
        )

    logger.error("")
    logger.error("!! Caught Exception !!")
    logger.error(tb)

    if message is not None:
        logger.error("")
        logger.error("Message:")
        logger.error(message)

    if data is not None:
        logger.error("")
        logger.error("Data:")
        logger.error(pformat(data))
