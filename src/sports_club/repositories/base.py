"""Базовый репозиторий для доменных сущностей."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sports_club.core.exceptions import DuplicateError, NotFoundError

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Общий CRUD-контракт. Хранит объекты в памяти, персистит через storage."""

    def __init__(self) -> None:
        self._items: dict[int, T] = {}

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
            raise NotFoundError(f"Объект с id={id_} не найден")
        return self._items[id_]

    def list(self) -> list[T]:
        return list(self._items.values())

    def add(self, item: T) -> None:
        id_ = self._get_id(item)
        if id_ in self._items:
            raise DuplicateError(f"Объект с id={id_} уже существует")
        self._items[id_] = item
        self.save()

    def update(self, item: T) -> None:
        id_ = self._get_id(item)
        if id_ not in self._items:
            raise NotFoundError(f"Объект с id={id_} не найден")
        self._items[id_] = item
        self.save()

    def delete(self, id_: int) -> None:
        self.get(id_)
        del self._items[id_]
        self.save()

    def next_id(self) -> int:
        return max(self._items, default=0) + 1

    def _dump(self) -> list[dict]:
        return [self._to_dict(item) for item in self._items.values()]

    def _load_from(self, data: list[dict]) -> None:
        self._items = {self._get_id(item := self._from_dict(d)): item
                       for d in data}