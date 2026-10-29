"""Репозиторий записей спортсменов в секции."""
from __future__ import annotations

from sports_club.core import config
from sports_club.models.enrollment import Enrollment
from sports_club.models.serialization import enrollment_from_dict
from sports_club.repositories.base import BaseRepository
from sports_club.repositories.storage.json_storage import JsonStorage
from sports_club.repositories.storage.xml_storage import XmlStorage


class EnrollmentRepository(BaseRepository[Enrollment]):
    def __init__(self) -> None:
        super().__init__()
        self._json = JsonStorage(config.ENROLLMENTS_JSON)
        self._xml = XmlStorage(
            config.ENROLLMENTS_XML, root="enrollments", item="enrollment"
        )

    @staticmethod
    def _get_id(item: Enrollment) -> int:
        return item.id

    def _to_dict(self, item: Enrollment) -> dict:
        return item.to_dict()

    def _from_dict(self, d: dict) -> Enrollment:
        return enrollment_from_dict(d)

    def save(self) -> None:
        data = self._dump()
        self._json.write(data)
        self._xml.write(data)

    def load(self) -> None:
        data = self._json.read()
        if not data:
            data = self._xml.read()
        self._load_from(data)