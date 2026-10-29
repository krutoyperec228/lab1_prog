"""Фабрики объектов из словарей (для JSON/XML)."""
from __future__ import annotations

from datetime import date
from typing import Any

from sports_club.models.enrollment import Enrollment
from sports_club.models.person import Athlete, Coach
from sports_club.models.section import Section


def coach_from_dict(d: dict[str, Any]) -> Coach:
    return Coach(
        cid=int(d["id"]),
        name=str(d["name"]),
        age=int(d["age"]),
        phone=str(d["phone"]),
        specialization=str(d["specialization"]),
        experience=int(d["experience"]),
    )


def athlete_from_dict(d: dict[str, Any]) -> Athlete:
    return Athlete(
        aid=int(d["id"]),
        name=str(d["name"]),
        age=int(d["age"]),
        phone=str(d["phone"]),
        category=str(d["category"]),
    )


def section_from_dict(d: dict[str, Any]) -> Section:
    return Section(
        sid=int(d["id"]),
        name=str(d["name"]),
        sport=str(d["sport"]),
        coach_id=int(d["coach_id"]),
        max_size=int(d["max_size"]),
        min_age=int(d.get("min_age", 6)),
    )


def enrollment_from_dict(d: dict[str, Any]) -> Enrollment:
    return Enrollment(
        eid=int(d["id"]),
        athlete_id=int(d["athlete_id"]),
        section_id=int(d["section_id"]),
        enrolled_at=date.fromisoformat(str(d["enrolled_at"])),
        status=str(d.get("status", "active")),
        monthly_fee=float(d.get("monthly_fee", 0.0)),
    )