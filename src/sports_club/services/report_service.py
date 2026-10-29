"""Прикладные отчёты по клубу."""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime

from sports_club.core.config import REPORTS_DIR
from sports_club.repositories.athlete_repository import AthleteRepository
from sports_club.repositories.enrollment_repository import EnrollmentRepository
from sports_club.repositories.section_repository import SectionRepository


class ReportService:
    def __init__(
        self,
        athletes: AthleteRepository,
        sections: SectionRepository,
        enrollments: EnrollmentRepository,
    ) -> None:
        self._athletes = athletes
        self._sections = sections
        self._enrollments = enrollments

    def _active_per_section(self) -> Counter[int]:
        return Counter(
            e.section_id
            for e in self._enrollments.list()
            if e.status == "active"
        )

    def load_report(self) -> list[str]:
        """Отчёт по загрузке секций: used/max (процент)."""
        active = self._active_per_section()
        lines: list[str] = []
        # сортируем по убыванию заполненности
        for s in sorted(
            self._sections.list(), key=lambda x: -active.get(x.id, 0)
        ):
            used = active.get(s.id, 0)
            pct = (used / s.max_size * 100) if s.max_size else 0.0
            lines.append(
                f"{s.name:35} {used:3}/{s.max_size:<3} ({pct:5.1f}%)"
            )
        return lines

    def free_slots(self) -> list[str]:
        """Секции, где есть свободные места."""
        active = self._active_per_section()
        result: list[str] = []
        for s in self._sections.list():
            free = s.max_size - active.get(s.id, 0)
            if free > 0:
                result.append(f"{s.name}: {free} мест")
        return result

    def revenue(self) -> float:
        """Суммарный доход по активным записям (руб./мес)."""
        return sum(
            e.monthly_fee
            for e in self._enrollments.list()
            if e.status == "active"
        )

    def age_groups(self) -> dict[str, int]:
        """Распределение спортсменов по возрастным группам."""
        groups = {"6-9": 0, "10-13": 0, "14-17": 0, "18+": 0}
        for a in self._athletes.list():
            if a.age < 10:
                groups["6-9"] += 1
            elif a.age < 14:
                groups["10-13"] += 1
            elif a.age < 18:
                groups["14-17"] += 1
            else:
                groups["18+"] += 1
        return groups

    def athletes_without_sections(self) -> list[str]:
        """Спортсмены без активной записи ни в одну секцию."""
        enrolled = {
            e.athlete_id
            for e in self._enrollments.list()
            if e.status == "active"
        }
        return [
            f"#{a.id} {a.name}"
            for a in self._athletes.list()
            if a.id not in enrolled
        ]

    def export_report(self) -> str:
        """Сохраняет сводный отчёт в data/reports/ и возвращает путь."""
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = REPORTS_DIR / f"report_{stamp}.json"

        data = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "load": self.load_report(),
            "free_slots": self.free_slots(),
            "revenue": round(self.revenue(), 2),
            "age_groups": self.age_groups(),
            "athletes_without_sections": self.athletes_without_sections(),
        }
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return str(path)