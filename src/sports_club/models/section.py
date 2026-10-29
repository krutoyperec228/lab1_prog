"""Модель секции."""
from __future__ import annotations

from typing import Any

from sports_club.core.exceptions import ValidationError


class Section:
    """Секция: название, вид спорта, тренер, лимит, минимальный возраст."""

    def __init__(
        self,
        sid: int,
        name: str,
        sport: str,
        coach_id: int,
        max_size: int,
        min_age: int = 6,
    ) -> None:
        if not name or not name.strip():
            raise ValidationError("Название секции обязательно")
        if not sport or not sport.strip():
            raise ValidationError("Вид спорта обязателен")
        if max_size <= 0:
            raise ValidationError("Макс. участников должно быть > 0")
        if min_age < 0:
            raise ValidationError("Минимальный возраст не может быть < 0")
        self._id = sid
        self._name = name.strip()
        self._sport = sport.strip()
        self._coach_id = coach_id
        self._max_size = max_size
        self._min_age = min_age

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def sport(self) -> str:
        return self._sport

    @property
    def coach_id(self) -> int:
        return self._coach_id

    @property
    def max_size(self) -> int:
        return self._max_size

    @property
    def min_age(self) -> int:
        return self._min_age

    def get_info(self) -> str:
        return (
            f"[Секция #{self._id}] {self._name} ({self._sport}), "
            f"тренер #{self._coach_id}, мест: {self._max_size}, "
            f"с {self._min_age} лет"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self._id,
            "name": self._name,
            "sport": self._sport,
            "coach_id": self._coach_id,
            "max_size": self._max_size,
            "min_age": self._min_age,
        }