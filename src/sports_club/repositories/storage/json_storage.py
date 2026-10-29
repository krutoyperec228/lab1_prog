"""Атомарное чтение/запись JSON-массива."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sports_club.core.exceptions import StorageError


class JsonStorage:
    """Хранит список словарей в JSON-файле."""

    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    def exists(self) -> bool:
        return self._path.exists()

    def read(self) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        try:
            with self._path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise StorageError(f"Не удалось прочитать {self._path}: {e}") from e
        if not isinstance(data, list):
            raise StorageError(f"{self._path}: ожидался JSON-массив")
        return data

    def write(self, data: list[dict[str, Any]]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(self._path.suffix + ".tmp")
        try:
            with tmp.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            tmp.replace(self._path)  # атомарная замена
        except OSError as e:
            raise StorageError(f"Не удалось записать {self._path}: {e}") from e