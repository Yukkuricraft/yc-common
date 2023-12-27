import shutil
import os
from typing import Optional

from src.common.logger_setup import logger


def recursive_chown(path, uid: Optional[int] = None, gid: Optional[int] = None):
    if uid is None and gid is None:
        raise ValueError(f"You must provide a UID, GID, or both but not")

    logger.info(">> RECURSIVELY CHOWNING ")
    logger.info(path)
    for dirpath, _, filenames in os.walk(path):
        logger.info(dirpath)
        shutil.chown(dirpath, uid, gid)
        for filename in filenames:
            shutil.chown(os.path.join(dirpath, filename), uid, gid)


def recursive_chmod(path, mode: int):
    # Should really validate mode.

    logger.info(">> RECURSIVELY CHMODDING ")
    logger.info(path)
    for dirpath, _, filenames in os.walk(path):
        logger.info(dirpath)
        os.chmod(dirpath, mode)
        for filename in filenames:
            os.chmod(os.path.join(dirpath, filename), mode)
