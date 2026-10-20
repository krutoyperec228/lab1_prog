"""Модели предметной области спортивного клуба и свои исключения."""
from typing import Any, Optional


# СВОИ ИСКЛЮЧЕНИЯ
class SportsClubError(Exception):
    """Базовое исключение для всех ошибок спортивного клуба."""


class NotFoundError(SportsClubError):
    """Сущность с указанным id не найдена."""


class DuplicateError(SportsClubError):
    """Попытка добавить сущность с уже существующим id."""


class SectionFullError(SportsClubError):
    """Попытка записать спортсмена в заполненную секцию."""


class ValidationError(SportsClubError):
    """Некорректные данные при создании объекта."""


# МОДЕЛИ
class Person:
    """Базовый класс человека: ФИО, возраст, телефон."""

    def __init__(self, name: str, age: int, phone: str) -> None:
        if not name or age <= 0 or age > 100:
            raise ValidationError("Некорректные данные человека")
        self._name = name
        self._age = age
        self._phone = phone

    def get_info(self) -> str:
        return f"{self._name}, {self._age} лет, тел.: {self._phone}"

    def to_dict(self) -> dict[str, Any]:
        return {"name": self._name, "age": self._age, "phone": self._phone}


class Coach(Person):
    """Тренер: человек с id, специализацией и стажем."""

    def __init__(self, cid: int, name: str, age: int, phone: str,
                 specialization: str, experience: int) -> None:
        super().__init__(name, age, phone)
        self._id = cid
        self._specialization = specialization
        self._experience = experience

    def get_info(self) -> str:
        return (f"[Тренер #{self._id}] {super().get_info()}, "
                f"{self._specialization}, стаж {self._experience} лет")

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update({"id": self._id,
                  "specialization": self._specialization,
                  "experience": self._experience})
        return d


class Athlete(Person):
    """Спортсмен: человек с id, разрядом и списком секций."""

    def __init__(self, aid: int, name: str, age: int, phone: str,
                 category: str,
                 section_ids: Optional[list[int]] = None) -> None:
        super().__init__(name, age, phone)
        self._id = aid
        self._category = category
        self._section_ids = list(section_ids) if section_ids else []

    def get_name(self) -> str:
        return self._name

    def has_section(self, sid: int) -> bool:
        return sid in self._section_ids

    def add_section(self, sid: int) -> None:
        if sid not in self._section_ids:
            self._section_ids.append(sid)

    def get_info(self) -> str:
        return (f"[Спортсмен #{self._id}] {super().get_info()}, "
                f"разряд: {self._category}, секции: {self._section_ids}")

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update({"id": self._id,
                  "category": self._category,
                  "section_ids": self._section_ids})
        return d


class Section:
    """Секция: название, вид спорта, тренер, лимит и список спортсменов."""

    def __init__(self, sid: int, name: str, sport: str, coach_id: int,
                 max_size: int,
                 athlete_ids: Optional[list[int]] = None) -> None:
        if not name or not sport:
            raise ValidationError("Название и вид спорта секции обязательны")
        if max_size <= 0:
            raise ValidationError("Макс. участников должно быть > 0")
        self._id = sid
        self._name = name
        self._sport = sport
        self._coach_id = coach_id
        self._max_size = max_size
        self._athlete_ids = list(athlete_ids) if athlete_ids else []

    def get_name(self) -> str:
        return self._name

    def add_athlete(self, athlete_id: int) -> None:
        if len(self._athlete_ids) >= self._max_size:
            raise SectionFullError(
                f"Секция '{self._name}' заполнена ({self._max_size} мест)")
        if athlete_id in self._athlete_ids:
            raise DuplicateError("Спортсмен уже в этой секции")
        self._athlete_ids.append(athlete_id)

    def get_info(self) -> str:
        return (f"[Секция #{self._id}] {self._name} ({self._sport}), "
                f"тренер #{self._coach_id}, участников "
                f"{len(self._athlete_ids)}/{self._max_size}")

    def to_dict(self) -> dict[str, Any]:
        return {"id": self._id, "name": self._name, "sport": self._sport,
                "coach_id": self._coach_id, "max_size": self._max_size,
                "athlete_ids": self._athlete_ids}


#
def coach_from_dict(d: dict[str, Any]) -> Coach:
    """Создаёт тренера из словаря."""
    return Coach(
        int(d["id"]),
        str(d["name"]),
        int(d["age"]),
        str(d["phone"]),
        str(d["specialization"]),
        int(d["experience"]),
    )


def athlete_from_dict(d: dict[str, Any]) -> Athlete:
    """Создаёт спортсмена из словаря."""
    return Athlete(
        int(d["id"]),
        str(d["name"]),
        int(d["age"]),
        str(d["phone"]),
        str(d["category"]),
        [int(x) for x in d.get("section_ids", [])],
    )


def section_from_dict(d: dict[str, Any]) -> Section:
    """Создаёт секцию из словаря."""
    return Section(
        int(d["id"]),
        str(d["name"]),
        str(d["sport"]),
        int(d["coach_id"]),
        int(d["max_size"]),
        [int(x) for x in d.get("athlete_ids", [])],
    )