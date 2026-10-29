"""Базовый класс человека, тренер и спортсмен."""
from __future__ import annotations

from typing import Any

from sports_club.core.exceptions import ValidationError


class Person:
    """Человек: ФИО, возраст, телефон."""

    def __init__(self, name: str, age: int, phone: str) -> None:
        if not name or not name.strip():
            raise ValidationError("ФИО не может быть пустым")
        if not (1 <= age <= 100):
            raise ValidationError(f"Возраст должен быть 1..100, получено {age}")
        self._name = name.strip()
        self._age = age
        self._phone = phone

    @property
    def name(self) -> str:
        return self._name

    @property
    def age(self) -> int:
        return self._age

    @property
    def phone(self) -> str:
        return self._phone

    def get_info(self) -> str:
        return f"{self._name}, {self._age} лет, тел.: {self._phone}"

    def to_dict(self) -> dict[str, Any]:
        return {"name": self._name, "age": self._age, "phone": self._phone}


class Coach(Person):
    """Тренер: специализация и стаж."""

    def __init__(
        self,
        cid: int,
        name: str,
        age: int,
        phone: str,
        specialization: str,
        experience: int,
    ) -> None:
        super().__init__(name, age, phone)
        if experience < 0:
            raise ValidationError("Стаж не может быть отрицательным")
        self._id = cid
        self._specialization = specialization
        self._experience = experience

    @property
    def id(self) -> int:
        return self._id

    @property
    def specialization(self) -> str:
        return self._specialization

    @property
    def experience(self) -> int:
        return self._experience

    def get_info(self) -> str:
        return (
            f"[Тренер #{self._id}] {super().get_info()}, "
            f"{self._specialization}, стаж {self._experience} лет"
        )

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(
            {
                "id": self._id,
                "specialization": self._specialization,
                "experience": self._experience,
            }
        )
        return d


class Athlete(Person):
    """Спортсмен: разряд."""

    def __init__(
        self,
        aid: int,
        name: str,
        age: int,
        phone: str,
        category: str,
    ) -> None:
        super().__init__(name, age, phone)
        self._id = aid
        self._category = category

    @property
    def id(self) -> int:
        return self._id

    @property
    def category(self) -> str:
        return self._category

    def get_info(self) -> str:
        return (
            f"[Спортсмен #{self._id}] {super().get_info()}, "
            f"разряд: {self._category}"
        )

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update({"id": self._id, "category": self._category})
        return d