import logging
from logging.handlers import RotatingFileHandler

LOG_FILENAME = "app.log"
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logger(name: str = None) -> logging.Logger:
    """
    Configure and return a logger.
    If 'name' is None, returns the root logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        # Logging format  
        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

        # File Handler
        file_handler = RotatingFileHandler(
            filename=LOG_FILENAME,
            maxBytes=5 * 1024 * 1024,
            backupCount=5
        )
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)

        # Adding both
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger