"""Настройка логирования в файл data/club.log."""
from __future__ import annotations

import logging
from pathlib import Path

LOG_FILE = Path("data/club.log")


def setup_logging(level: int = logging.INFO) -> None:
    """Инициализирует корневой логгер (один раз)."""
    root = logging.getLogger()
    if root.handlers:
        return

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    root.setLevel(level)
    root.addHandler(file_handler)
    root.addHandler(console_handler)