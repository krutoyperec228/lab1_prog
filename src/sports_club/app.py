"""Composition root: сборка зависимостей и запуск приложения."""
from __future__ import annotations

import logging

from sports_club.core.logging import setup_logging
from sports_club.repositories.athlete_repository import AthleteRepository
from sports_club.repositories.coach_repository import CoachRepository
from sports_club.repositories.enrollment_repository import EnrollmentRepository
from sports_club.repositories.section_repository import SectionRepository
from sports_club.services.club_service import ClubService
from sports_club.services.enrollment_service import EnrollmentService
from sports_club.services.report_service import ReportService
from sports_club.ui.console import ConsoleApp

log = logging.getLogger(__name__)


def build_app() -> ConsoleApp:
    """Создаёт все репозитории, грузит данные, собирает сервисы и UI."""
    setup_logging()

    coaches = CoachRepository()
    athletes = AthleteRepository()
    sections = SectionRepository()
    enrollments = EnrollmentRepository()

    for repo, label in (
        (coaches, "тренеры"),
        (athletes, "спортсмены"),
        (sections, "секции"),
        (enrollments, "записи"),
    ):
        try:
            repo.load()
        except Exception as e:
            log.exception("Не удалось загрузить %s: %s", label, e)
            print(f"Предупреждение: не удалось загрузить {label} ({e}).")

    club = ClubService(coaches, athletes, sections)
    enroll_svc = EnrollmentService(athletes, sections, enrollments)
    reports = ReportService(athletes, sections, enrollments)

    return ConsoleApp(club=club, enrollments=enroll_svc, reports=reports)


def run() -> None:
    app = build_app()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nПрерывание с клавиатуры. Выход.")