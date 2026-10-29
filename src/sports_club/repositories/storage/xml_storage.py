"""Атомарное чтение/запись XML-списка."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from xml.dom import minidom

from sports_club.core.exceptions import StorageError


class XmlStorage:
    """Хранит список словарей в XML-файле.

    Структура: <root><item>{field: text}</item>...</root>,
    где поле id выносится в атрибут.
    """

    def __init__(self, path: Path, root: str, item: str) -> None:
        self._path = path
        self._root_tag = root
        self._item_tag = item

    @property
    def path(self) -> Path:
        return self._path

    def exists(self) -> bool:
        return self._path.exists()

    def read(self) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        try:
            tree = ET.parse(self._path)
        except (OSError, ET.ParseError) as e:
            raise StorageError(f"Не удалось прочитать {self._path}: {e}") from e
        result: list[dict[str, Any]] = []
        for el in tree.getroot().findall(self._item_tag):
            d: dict[str, Any] = dict(el.attrib)
            for child in el:
                d[child.tag] = (child.text or "").strip()
            result.append(d)
        return result

    def write(self, data: list[dict[str, Any]]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        root = ET.Element(self._root_tag)
        for d in data:
            item = ET.SubElement(root, self._item_tag)
            for key, value in d.items():
                if key == "id":
                    item.set("id", str(value))
                else:
                    ET.SubElement(item, key).text = str(value)
        pretty = minidom.parseString(
            ET.tostring(root, encoding="unicode")
        ).toprettyxml(indent="  ")
        tmp = self._path.with_suffix(self._path.suffix + ".tmp")
        try:
            with tmp.open("w", encoding="utf-8") as f:
                f.write(pretty)
            tmp.replace(self._path)
        except OSError as e:
            raise StorageError(f"Не удалось записать {self._path}: {e}") from e