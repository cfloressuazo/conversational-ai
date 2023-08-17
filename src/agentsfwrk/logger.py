import logging
import multiprocessing
import sys

APP_LOGGER_NAME = 'CaiApp'

def setup_applevel_logger(logger_name = APP_LOGGER_NAME, file_name = None):
    """
    Setup the logger for the application
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(sh)
    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

def get_multiprocessing_logger(file_name = None):
    """
    Setup the logger for the application for multiprocessing
    """
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)

    if not len(logger.handlers):
        logger.addHandler(sh)

    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger



def get_logger(module_name, logger_name = None):
    """
    Get the logger for the module
    """
    return logging.getLogger(logger_name or APP_LOGGER_NAME).getChild(module_name)
