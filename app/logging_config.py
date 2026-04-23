"""Настройка логирования приложения.

Логи пишутся одновременно в stdout и в файл (LOG_FILE).
"""

from __future__ import annotations

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from app.config import settings

_LOGGER_NAME = "blogicum"
_CONFIGURED = False


def setup_logging() -> logging.Logger:
    """Инициализировать корневой логгер приложения."""
    global _CONFIGURED
    logger = logging.getLogger(_LOGGER_NAME)

    if _CONFIGURED:
        return logger

    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    log_path = settings.log_file
    log_dir = os.path.dirname(log_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    _CONFIGURED = True
    return logger


def get_logger() -> logging.Logger:
    """Получить логгер приложения (инициализируя при первом вызове)."""
    return setup_logging()
