import logging

logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter: logging.Formatter = logging.Formatter(
    "[%(asctime)s][%(levelname)s] %(message)s"
)

ch: logging.StreamHandler = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

logger.info(f"LOGGING INITIALIZED - {__name__}")
