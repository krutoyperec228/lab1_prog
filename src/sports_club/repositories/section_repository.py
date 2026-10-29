"""Репозиторий секций."""
from __future__ import annotations

from sports_club.core import config
from sports_club.models.section import Section
from sports_club.models.serialization import section_from_dict
from sports_club.repositories.base import BaseRepository
from sports_club.repositories.storage.json_storage import JsonStorage
from sports_club.repositories.storage.xml_storage import XmlStorage


class SectionRepository(BaseRepository[Section]):
    def __init__(self) -> None:
        super().__init__()
        self._json = JsonStorage(config.SECTIONS_JSON)
        self._xml = XmlStorage(
            config.SECTIONS_XML, root="sections", item="section"
        )

    @staticmethod
    def _get_id(item: Section) -> int:
        return item.id

    def _to_dict(self, item: Section) -> dict:
        return item.to_dict()

    def _from_dict(self, d: dict) -> Section:
        return section_from_dict(d)

    def save(self) -> None:
        data = self._dump()
        self._json.write(data)
        self._xml.write(data)

    def load(self) -> None:
        data = self._json.read()
        if not data:
            data = self._xml.read()
        self._load_from(data)