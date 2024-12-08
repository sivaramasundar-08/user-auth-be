import sys

import loguru


def loggers_data():
    logger = loguru.logger
    logger.remove()
    logger.add(sys.stdout, format="{time} - {level} - ({extra[request_id]}) {message} ", level="DEBUG")
    return logger


logger = loggers_data()
