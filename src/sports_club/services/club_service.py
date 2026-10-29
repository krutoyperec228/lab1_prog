"""Бизнес-логика клуба: CRUD и проверка ссылок."""
from __future__ import annotations

from sports_club.core.exceptions import (
    SportsClubError,
    ValidationError,
)
from sports_club.models.person import Athlete, Coach
from sports_club.models.section import Section
from sports_club.repositories.athlete_repository import AthleteRepository
from sports_club.repositories.coach_repository import CoachRepository
from sports_club.repositories.section_repository import SectionRepository


class ClubService:
    """Согласует действия между репозиториями тренеров/спортсменов/секций."""

    def __init__(
        self,
        coaches: CoachRepository,
        athletes: AthleteRepository,
        sections: SectionRepository,
    ) -> None:
        self._coaches = coaches
        self._athletes = athletes
        self._sections = sections

    def add_coach(self, coach: Coach) -> None:
        self._coaches.add(coach)

    def get_coach(self, cid: int) -> Coach:
        return self._coaches.get(cid)

    def list_coaches(self) -> list[Coach]:
        return self._coaches.list()

    def delete_coach(self, cid: int) -> None:
        self._coaches.get(cid)
        for section in self._sections.list():
            if section.coach_id == cid:
                raise SportsClubError(
                    f"Тренер #{cid} ведёт секцию '{section.name}'. "
                    f"Сначала удалите секцию."
                )
        self._coaches.delete(cid)

    def add_athlete(self, athlete: Athlete) -> None:
        self._athletes.add(athlete)

    def get_athlete(self, aid: int) -> Athlete:
        return self._athletes.get(aid)

    def list_athletes(self) -> list[Athlete]:
        return self._athletes.list()

    def delete_athlete(self, aid: int) -> None:
        self._athletes.get(aid)
        self._athletes.delete(aid)

    def add_section(self, section: Section) -> None:
        self._coaches.get(section.coach_id)
        self._sections.add(section)

    def get_section(self, sid: int) -> Section:
        return self._sections.get(sid)

    def list_sections(self) -> list[Section]:
        return self._sections.list()

    def delete_section(self, sid: int) -> None:
        self._sections.delete(sid)

    def check_links(self) -> None:
        coaches = {c.id for c in self._coaches.list()}
        athletes = {a.id for a in self._athletes.list()}
        for s in self._sections.list():
            if s.coach_id not in coaches:
                raise ValidationError(
                    f"Секция #{s.id} ссылается на тренера #{s.coach_id}"
                )
        _ = athletes