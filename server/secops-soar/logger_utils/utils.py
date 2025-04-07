import logging

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s",  # Include logger name
)


def get_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    return logger
