"""Модель записи спортсмена в секцию."""
from __future__ import annotations

from datetime import date
from typing import Any

from sports_club.core.exceptions import ValidationError

VALID_STATUSES = ("active", "paused", "completed")


class Enrollment:
    """Запись: кто, куда, когда, в каком статусе, сколько платит."""

    def __init__(
        self,
        eid: int,
        athlete_id: int,
        section_id: int,
        enrolled_at: date,
        status: str = "active",
        monthly_fee: float = 0.0,
    ) -> None:
        if status not in VALID_STATUSES:
            raise ValidationError(f"Недопустимый статус: {status}")
        if monthly_fee < 0:
            raise ValidationError("Оплата не может быть отрицательной")
        self._id = eid
        self._athlete_id = athlete_id
        self._section_id = section_id
        self._enrolled_at = enrolled_at
        self._status = status
        self._monthly_fee = monthly_fee

    @property
    def id(self) -> int:
        return self._id

    @property
    def athlete_id(self) -> int:
        return self._athlete_id

    @property
    def section_id(self) -> int:
        return self._section_id

    @property
    def enrolled_at(self) -> date:
        return self._enrolled_at

    @property
    def status(self) -> str:
        return self._status

    @property
    def monthly_fee(self) -> float:
        return self._monthly_fee

    def set_status(self, status: str) -> None:
        if status not in VALID_STATUSES:
            raise ValidationError(f"Недопустимый статус: {status}")
        self._status = status

    def get_info(self) -> str:
        return (
            f"[Запись #{self._id}] спортсмен #{self._athlete_id} → "
            f"секция #{self._section_id}, {self._enrolled_at.isoformat()}, "
            f"статус: {self._status}, {self._monthly_fee:.2f} руб./мес"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self._id,
            "athlete_id": self._athlete_id,
            "section_id": self._section_id,
            "enrolled_at": self._enrolled_at.isoformat(),
            "status": self._status,
            "monthly_fee": self._monthly_fee,
        }