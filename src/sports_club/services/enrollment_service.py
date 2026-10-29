"""Запись спортсменов в секции и управление статусами."""
from __future__ import annotations

from datetime import date

from sports_club.core.exceptions import (
    DuplicateError,
    NotFoundError,
    SectionFullError,
    ValidationError,
)
from sports_club.models.enrollment import Enrollment
from sports_club.repositories.athlete_repository import AthleteRepository
from sports_club.repositories.enrollment_repository import EnrollmentRepository
from sports_club.repositories.section_repository import SectionRepository


class EnrollmentService:
    def __init__(
        self,
        athletes: AthleteRepository,
        sections: SectionRepository,
        enrollments: EnrollmentRepository,
    ) -> None:
        self._athletes = athletes
        self._sections = sections
        self._enrollments = enrollments

    def _active_count(self, section_id: int) -> int:
        return sum(
            1
            for e in self._enrollments.list()
            if e.section_id == section_id and e.status == "active"
        )

    def enroll(
        self, athlete_id: int, section_id: int, monthly_fee: float = 0.0
    ) -> Enrollment:
        athlete = self._athletes.get(athlete_id)
        section = self._sections.get(section_id)

        for e in self._enrollments.list():
            if (
                e.athlete_id == athlete_id
                and e.section_id == section_id
                and e.status == "active"
            ):
                raise DuplicateError("Спортсмен уже записан в эту секцию")

        if self._active_count(section_id) >= section.max_size:
            raise SectionFullError(
                f"Секция '{section.name}' заполнена ({section.max_size} мест)"
            )

        if athlete.age < section.min_age:
            raise ValidationError(
                f"Спортсмен младше минимального возраста "
                f"({section.min_age} лет) для секции '{section.name}'"
            )

        enrollment = Enrollment(
            eid=self._enrollments.next_id(),
            athlete_id=athlete_id,
            section_id=section_id,
            enrolled_at=date.today(),
            status="active",
            monthly_fee=monthly_fee,
        )
        self._enrollments.add(enrollment)
        return enrollment

    def set_status(self, enrollment_id: int, status: str) -> Enrollment:
        e = self._enrollments.get(enrollment_id)
        e.set_status(status)
        self._enrollments.update(e)
        return e

    def list_enrollments(self) -> list[Enrollment]:
        return self._enrollments.list()

    def get(self, enrollment_id: int) -> Enrollment:
        return self._enrollments.get(enrollment_id)

    def delete(self, enrollment_id: int) -> None:
        self._enrollments.delete(enrollment_id)

    def athlete_sections(self, athlete_id: int) -> list[str]:
        """Названия секций, куда записан спортсмен."""
        self._athletes.get(athlete_id)
        result: list[str] = []
        for e in self._enrollments.list():
            if e.athlete_id == athlete_id and e.status == "active":
                try:
                    result.append(self._sections.get(e.section_id).name)
                except NotFoundError:
                    continue
        return result