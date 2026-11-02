"""Базовый репозиторий для доменных сущностей."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sports_club.core.exceptions import DuplicateError, NotFoundError

log = logging.getLogger(__name__)
T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Общий CRUD-контракт. Хранит объекты в памяти, персистит через storage."""

    entity: str = "object"

    def __init__(self) -> None:
        self._items: dict[int, T] = {}
        self._next_id: int = 1

    @staticmethod
    @abstractmethod
    def _get_id(item: T) -> int: ...

    @abstractmethod
    def _to_dict(self, item: T) -> dict: ...

    @abstractmethod
    def _from_dict(self, d: dict) -> T: ...

    @abstractmethod
    def save(self) -> None: ...

    @abstractmethod
    def load(self) -> None: ...

    def get(self, id_: int) -> T:
        if id_ not in self._items:
            log.warning("%s: id=%s не найден", self.entity, id_)
            raise NotFoundError(f"Объект с id={id_} не найден")
        return self._items[id_]

    def list(self) -> list[T]:
        return list(self._items.values())

    def add(self, item: T) -> None:
        id_ = self._get_id(item)
        if id_ == 0:
            id_ = self.next_id()
            if hasattr(item, "set_id"):
                item.set_id(id_)
        if id_ in self._items:
            log.warning("%s: id=%s уже существует", self.entity, id_)
            raise DuplicateError(f"Объект с id={id_} уже существует")
        self._items[id_] = item
        if id_ >= self._next_id:
            self._next_id = id_ + 1
        log.info("%s: добавлен id=%s", self.entity, id_)
        self.save()

    def update(self, item: T) -> None:
        id_ = self._get_id(item)
        if id_ not in self._items:
            log.warning("%s: id=%s не найден для обновления", self.entity, id_)
            raise NotFoundError(f"Объект с id={id_} не найден")
        self._items[id_] = item
        log.info("%s: обновлён id=%s", self.entity, id_)
        self.save()

    def delete(self, id_: int) -> None:
        self.get(id_)
        del self._items[id_]
        log.info("%s: удалён id=%s", self.entity, id_)
        self.save()

    def next_id(self) -> int:
        """Возвращает следующий свободный id и сдвигает счётчик."""
        id_ = self._next_id
        self._next_id += 1
        return id_

    def _dump(self) -> list[dict]:
        return [self._to_dict(item) for item in self._items.values()]

    def _load_from(self, data: list[dict]) -> None:
        self._items = {self._get_id(item := self._from_dict(d)): item
                       for d in data}
        max_id = max(self._items, default=0)
        self._next_id = max(self._next_id, max_id + 1)
        log.info(
            "%s: загружено %d записей (next_id=%d)",
            self.entity, len(self._items), self._next_id,
        )