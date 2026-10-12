from __future__ import annotations
from typing import Any, Optional


# ---------- СВОИ ИСКЛЮЧЕНИЯ ----------
class SportsClubError(Exception):
    pass


class NotFoundError(SportsClubError):
    pass


class DuplicateError(SportsClubError):
    pass


class SectionFullError(SportsClubError):
    pass


class ValidationError(SportsClubError):
    pass


# ---------- МОДЕЛИ ----------
class Person:
    def __init__(self, name: str, age: int, phone: str) -> None:
        if not name or age <= 0 or age > 100:
            raise ValidationError("Некорректные данные человека")
        self._name: str = name
        self._age: int = age
        self._phone: str = phone

    def get_info(self) -> str:
        return f"{self._name}, {self._age} лет, тел.: {self._phone}"

    def to_dict(self) -> dict[str, Any]:
        return {"name": self._name, "age": self._age, "phone": self._phone}


class Coach(Person):
    def __init__(self, cid: int, name: str, age: int, phone: str,
                 specialization: str, experience: int) -> None:
        super().__init__(name, age, phone)
        self._id: int = cid
        self._specialization: str = specialization
        self._experience: int = experience

    def get_info(self) -> str:
        return (f"[Тренер #{self._id}] {super().get_info()}, "
                f"{self._specialization}, стаж {self._experience} лет")

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update({"id": self._id,
                  "specialization": self._specialization,
                  "experience": self._experience})
        return d

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "Coach":
        return Coach(
            int(d["id"]),
            str(d["name"]),
            int(d["age"]),
            str(d["phone"]),
            str(d["specialization"]),
            int(d["experience"]),
        )


class Athlete(Person):
    def __init__(self, aid: int, name: str, age: int, phone: str,
                 category: str,
                 section_ids: Optional[list[int]] = None) -> None:
        super().__init__(name, age, phone)
        self._id: int = aid
        self._category: str = category
        self._section_ids: list[int] = list(section_ids) if section_ids else []

    def get_info(self) -> str:
        return (f"[Спортсмен #{self._id}] {super().get_info()}, "
                f"разряд: {self._category}, секции: {self._section_ids}")

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update({"id": self._id,
                  "category": self._category,
                  "section_ids": self._section_ids})
        return d

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "Athlete":
        return Athlete(
            int(d["id"]),
            str(d["name"]),
            int(d["age"]),
            str(d["phone"]),
            str(d["category"]),
            [int(x) for x in d.get("section_ids", [])],
        )


class Section:
    def __init__(self, sid: int, name: str, sport: str, coach_id: int,
                 max_size: int,
                 athlete_ids: Optional[list[int]] = None) -> None:
        self._id: int = sid
        self._name: str = name
        self._sport: str = sport
        self._coach_id: int = coach_id
        self._max_size: int = max_size
        self._athlete_ids: list[int] = list(athlete_ids) if athlete_ids else []

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

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "Section":
        return Section(
            int(d["id"]),
            str(d["name"]),
            str(d["sport"]),
            int(d["coach_id"]),
            int(d["max_size"]),
            [int(x) for x in d.get("athlete_ids", [])],
        )