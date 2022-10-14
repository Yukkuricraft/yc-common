import shutil
import os

from src.common.logger_setup import logger

def recursive_chown(path, uid, gid):
    logger.info(">> RECURSIVELY CHOWNING ")
    logger.info(path)
    for dirpath, _, filenames in os.walk(path):
        logger.info(dirpath)
        shutil.chown(dirpath, uid, gid)
        for filename in filenames:
            shutil.chown(os.path.join(dirpath, filename), uid, gid)
