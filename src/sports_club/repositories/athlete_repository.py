"""Репозиторий спортсменов."""
from __future__ import annotations

from sports_club.core import config
from sports_club.models.person import Athlete
from sports_club.models.serialization import athlete_from_dict
from sports_club.repositories.base import BaseRepository
from sports_club.repositories.storage.json_storage import JsonStorage
from sports_club.repositories.storage.xml_storage import XmlStorage


class AthleteRepository(BaseRepository[Athlete]):
    def __init__(self) -> None:
        super().__init__()
        self._json = JsonStorage(config.ATHLETES_JSON)
        self._xml = XmlStorage(
            config.ATHLETES_XML, root="athletes", item="athlete"
        )

    @staticmethod
    def _get_id(item: Athlete) -> int:
        return item.id

    def _to_dict(self, item: Athlete) -> dict:
        return item.to_dict()

    def _from_dict(self, d: dict) -> Athlete:
        return athlete_from_dict(d)

    def save(self) -> None:
        data = self._dump()
        self._json.write(data)
        self._xml.write(data)

    def load(self) -> None:
        data = self._json.read()
        if not data:
            data = self._xml.read()
        self._load_from(data)