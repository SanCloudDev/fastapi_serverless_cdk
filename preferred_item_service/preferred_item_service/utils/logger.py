import logging 
import typing
from fastapi.middleware import Middleware


def custom_logger(name):
    """
    Returns a custom logger with the specified name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to console handler
    ch.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(ch)

    return logger
