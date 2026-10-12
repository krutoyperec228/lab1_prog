from __future__ import annotations
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Any
from models import (Coach, Athlete, Section,
                    NotFoundError, DuplicateError, SportsClubError)


class SportsClub:
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._coaches: dict[int, Coach] = {}
        self._athletes: dict[int, Athlete] = {}
        self._sections: dict[int, Section] = {}

    # ---------- CRUD: Тренеры ----------
    def add_coach(self, coach: Coach) -> None:
        if coach._id in self._coaches:
            raise DuplicateError(f"Тренер с id={coach._id} уже есть")
        self._coaches[coach._id] = coach

    def get_coach(self, cid: int) -> Coach:
        if cid not in self._coaches:
            raise NotFoundError(f"Тренер с id={cid} не найден")
        return self._coaches[cid]

    def delete_coach(self, cid: int) -> None:
        self.get_coach(cid)
        for section in self._sections.values():
            if section._coach_id == cid:
                raise SportsClubError(
                    f"Тренер #{cid} ведёт секцию '{section._name}', "
                    f"сначала удалите секцию")
        del self._coaches[cid]

    # ---------- CRUD: Спортсмены ----------
    def add_athlete(self, athlete: Athlete) -> None:
        if athlete._id in self._athletes:
            raise DuplicateError(f"Спортсмен с id={athlete._id} уже есть")
        self._athletes[athlete._id] = athlete

    def get_athlete(self, aid: int) -> Athlete:
        if aid not in self._athletes:
            raise NotFoundError(f"Спортсмен с id={aid} не найден")
        return self._athletes[aid]

    def delete_athlete(self, aid: int) -> None:
        self.get_athlete(aid)
        for section in self._sections.values():
            if aid in section._athlete_ids:
                section._athlete_ids.remove(aid)
        del self._athletes[aid]

    # ---------- CRUD: Секции ----------
    def add_section(self, section: Section) -> None:
        if section._id in self._sections:
            raise DuplicateError(f"Секция с id={section._id} уже есть")
        if section._coach_id not in self._coaches:
            raise NotFoundError(f"Тренер id={section._coach_id} не найден")
        self._sections[section._id] = section

    def get_section(self, sid: int) -> Section:
        if sid not in self._sections:
            raise NotFoundError(f"Секция с id={sid} не найдена")
        return self._sections[sid]

    def delete_section(self, sid: int) -> None:
        self.get_section(sid)
        for athlete in self._athletes.values():
            if sid in athlete._section_ids:
                athlete._section_ids.remove(sid)
        del self._sections[sid]

    # ---------- JSON ----------
    def save_to_json(self, path: str) -> None:
        data: dict[str, Any] = {
            "name": self._name,
            "coaches": [c.to_dict() for c in self._coaches.values()],
            "athletes": [a.to_dict() for a in self._athletes.values()],
            "sections": [s.to_dict() for s in self._sections.values()],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_json(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)
        self._name = str(data.get("name", self._name))
        self._coaches = {int(c["id"]): Coach.from_dict(c)
                         for c in data.get("coaches", [])}
        self._athletes = {int(a["id"]): Athlete.from_dict(a)
                          for a in data.get("athletes", [])}
        self._sections = {int(s["id"]): Section.from_dict(s)
                          for s in data.get("sections", [])}

    # ---------- XML ----------
    def save_to_xml(self, path: str) -> None:
        root: ET.Element = ET.Element("club", name=self._name)

        coaches_el = ET.SubElement(root, "coaches")
        for c in self._coaches.values():
            el = ET.SubElement(coaches_el, "coach", id=str(c._id))
            ET.SubElement(el, "name").text = c._name
            ET.SubElement(el, "age").text = str(c._age)
            ET.SubElement(el, "phone").text = c._phone
            ET.SubElement(el, "specialization").text = c._specialization
            ET.SubElement(el, "experience").text = str(c._experience)

        athletes_el = ET.SubElement(root, "athletes")
        for a in self._athletes.values():
            el = ET.SubElement(athletes_el, "athlete", id=str(a._id))
            ET.SubElement(el, "name").text = a._name
            ET.SubElement(el, "age").text = str(a._age)
            ET.SubElement(el, "phone").text = a._phone
            ET.SubElement(el, "category").text = a._category
            ids_el = ET.SubElement(el, "section_ids")
            for sid in a._section_ids:
                ET.SubElement(ids_el, "id").text = str(sid)

        sections_el = ET.SubElement(root, "sections")
        for s in self._sections.values():
            el = ET.SubElement(sections_el, "section", id=str(s._id))
            ET.SubElement(el, "name").text = s._name
            ET.SubElement(el, "sport").text = s._sport
            ET.SubElement(el, "coach_id").text = str(s._coach_id)
            ET.SubElement(el, "max_size").text = str(s._max_size)
            ids_el = ET.SubElement(el, "athlete_ids")
            for aid in s._athlete_ids:
                ET.SubElement(ids_el, "id").text = str(aid)

        xml_str = ET.tostring(root, encoding="unicode")
        pretty = minidom.parseString(xml_str).toprettyxml(indent="  ")

        with open(path, "w", encoding="utf-8") as f:
            f.write(pretty)

    def load_from_xml(self, path: str) -> None:
        tree = ET.parse(path)
        root = tree.getroot()
        self._name = root.attrib.get("name", self._name)

        self._coaches = {}
        for el in root.findall("./coaches/coach"):
            cid = int(el.attrib["id"])
            self._coaches[cid] = Coach(
                cid,
                el.findtext("name"),
                int(el.findtext("age")),
                el.findtext("phone"),
                el.findtext("specialization"),
                int(el.findtext("experience")),
            )

        self._athletes = {}
        for el in root.findall("./athletes/athlete"):
            aid = int(el.attrib["id"])
            ids = [int(x.text) for x in el.findall("./section_ids/id")]
            self._athletes[aid] = Athlete(
                aid,
                el.findtext("name"),
                int(el.findtext("age")),
                el.findtext("phone"),
                el.findtext("category"),
                ids,
            )

        self._sections = {}
        for el in root.findall("./sections/section"):
            sid = int(el.attrib["id"])
            ids = [int(x.text) for x in el.findall("./athlete_ids/id")]
            self._sections[sid] = Section(
                sid,
                el.findtext("name"),
                el.findtext("sport"),
                int(el.findtext("coach_id")),
                int(el.findtext("max_size")),
                ids,
            )