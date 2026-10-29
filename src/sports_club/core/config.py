"""Пути к файлам данных и прочие константы."""
from __future__ import annotations

from pathlib import Path

DATA_DIR = Path("data")
REPORTS_DIR = DATA_DIR / "reports"

CLUB_META_JSON = DATA_DIR / "club.json"

COACHES_JSON = DATA_DIR / "coaches.json"
COACHES_XML = DATA_DIR / "coaches.xml"

ATHLETES_JSON = DATA_DIR / "athletes.json"
ATHLETES_XML = DATA_DIR / "athletes.xml"

SECTIONS_JSON = DATA_DIR / "sections.json"
SECTIONS_XML = DATA_DIR / "sections.xml"

ENROLLMENTS_JSON = DATA_DIR / "enrollments.json"
ENROLLMENTS_XML = DATA_DIR / "enrollments.xml"

DEFAULT_CLUB_NAME = "Олимп"