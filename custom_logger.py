import inspect
import logging
import datetime

def custom_logger(log_level=logging.DEBUG):
    logger_name = inspect.stack()[1][3]
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    file_handler = logging.FileHandler(filename=str(datetime.date.today()) + "_op-chapters.log", mode="a")
    file_handler.setLevel(log_level)

    formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                                  datefmt="%d%m%Y %I:%M:%S %p")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
