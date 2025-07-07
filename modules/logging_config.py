import logging
from logging.handlers import RotatingFileHandler

# Constants
LOG_FILENAME = "app.log"
LOG_LEVEL = logging.DEBUG
CONSOLE_LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 5

def setup_logger(name: str = None) -> logging.Logger:
    """
    Sets up a logger with both file and console output.

    Args:
        name (str): Logger name. If None, sets up the root logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

        # File Handler
        file_handler = RotatingFileHandler(
            filename=LOG_FILENAME,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(LOG_LEVEL)
        logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(CONSOLE_LOG_LEVEL)
        logger.addHandler(console_handler)

        logger.propagate = False # Prevent duplicate logs (if root logger also logs)

    return logger