import logging
import sys
from datetime import datetime
from pathlib import Path

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger("itau_performance")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
console_handler.setFormatter(console_formatter)

file_handler = logging.FileHandler(
    f"logs/app_{datetime.now().strftime('%Y%m%d')}.log", encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
file_handler.setFormatter(file_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_logger(name: str = "itau_performance"):
    """
    Retorna uma instância do logger

    Args:
        name: Nome do logger (opcional)

    Returns:
        Logger configurado
    """
    return logging.getLogger(name)


def log_info(message: str, **kwargs):
    """Log de informação"""
    extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
    if extra_info:
        logger.info(f"{message} | {extra_info}")
    else:
        logger.info(message)


def log_error(message: str, error: Exception = None, **kwargs):
    """Log de erro"""
    extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
    if error:
        logger.error(f"{message} | Error: {str(error)} | {extra_info}")
    else:
        logger.error(f"{message} | {extra_info}")


def log_warning(message: str, **kwargs):
    """Log de aviso"""
    extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
    if extra_info:
        logger.warning(f"{message} | {extra_info}")
    else:
        logger.warning(message)


def log_debug(message: str, **kwargs):
    """Log de debug"""
    extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
    if extra_info:
        logger.debug(f"{message} | {extra_info}")
    else:
        logger.debug(message)
