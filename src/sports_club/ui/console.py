"""Консольный интерфейс: меню, ввод, вывод, обработка ошибок."""
from __future__ import annotations

from sports_club.core.exceptions import (
    DuplicateError,
    NotFoundError,
    SectionFullError,
    SportsClubError,
    StorageError,
    ValidationError,
)
from sports_club.models.enrollment import Enrollment
from sports_club.models.person import Athlete, Coach
from sports_club.models.section import Section
from sports_club.services.club_service import ClubService
from sports_club.services.enrollment_service import EnrollmentService
from sports_club.services.report_service import ReportService


def read_int(prompt: str, min_value: int = 0) -> int:
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Ошибка: нужно целое число.")
            continue
        if value < min_value:
            print(f"Ошибка: значение должно быть не меньше {min_value}.")
            continue
        return value


def read_str(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Поле не может быть пустым.")


def read_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Ошибка: нужно число.")
            continue
        if value < 0:
            print("Ошибка: значение не может быть отрицательным.")
            continue
        return value


class ConsoleApp:
    """Главное меню и обработка пользовательского ввода."""

    def __init__(
        self,
        club: ClubService,
        enrollments: EnrollmentService,
        reports: ReportService,
    ) -> None:
        self._club = club
        self._enrollments = enrollments
        self._reports = reports

    def run(self) -> None:
        print("Спортивный клуб «Олимп»")
        while True:
            self._print_menu()
            choice = input("Выбор: ").strip()
            try:
                if not self._dispatch(choice):
                    break
            except ValidationError as e:
                print(f"Ошибка валидации: {e}")
            except DuplicateError as e:
                print(f"Дубликат: {e}")
            except NotFoundError as e:
                print(f"Не найдено: {e}")
            except SectionFullError as e:
                print(f"Секция переполнена: {e}")
            except StorageError as e:
                print(f"Ошибка файла: {e}")
            except SportsClubError as e:
                print(f"Ошибка клуба: {e}")
            except (ValueError, KeyError, TypeError) as e:
                print(f"Некорректные данные: {e}")
            except Exception as e:  # на случай совсем непредвиденного
                print(f"Непредвиденная ошибка: {e}")

    @staticmethod
    def _print_menu() -> None:
        print(
            "\n1.  Добавить тренера\n"
            "2.  Добавить спортсмена\n"
            "3.  Добавить секцию\n"
            "4.  Записать спортсмена в секцию\n"
            "5.  Удалить тренера\n"
            "6.  Удалить спортсмена\n"
            "7.  Удалить секцию\n"
            "8.  Показать всех тренеров\n"
            "9.  Показать всех спортсменов\n"
            "10. Показать все секции\n"
            "11. Показать все записи\n"
            "12. Сменить статус записи\n"
            "13. Отчёт: загрузка секций\n"
            "14. Отчёт: свободные места\n"
            "15. Отчёт: доход клуба\n"
            "16. Отчёт: возрастные группы\n"
            "17. Спортсмены без секций\n"
            "18. Экспортировать отчёт в файл\n"
            "0.  Выход"
        )

    def _dispatch(self, choice: str) -> bool:
        if choice == "0":
            print("До свидания!")
            return False

        if choice == "1":
            self._add_coach()
        elif choice == "2":
            self._add_athlete()
        elif choice == "3":
            self._add_section()
        elif choice == "4":
            self._enroll()
        elif choice == "5":
            cid = read_int("id тренера для удаления: ")
            self._club.delete_coach(cid)
            print(f"Тренер #{cid} удалён.")
        elif choice == "6":
            aid = read_int("id спортсмена для удаления: ")
            self._club.delete_athlete(aid)
            print(f"Спортсмен #{aid} удалён.")
        elif choice == "7":
            sid = read_int("id секции для удаления: ")
            self._club.delete_section(sid)
            print(f"Секция #{sid} удалена.")
        elif choice == "8":
            print("\n--- Тренеры ---")
            for c in self._club.list_coaches():
                print(c.get_info())
        elif choice == "9":
            print("\n--- Спортсмены ---")
            for a in self._club.list_athletes():
                print(a.get_info())
        elif choice == "10":
            print("\n--- Секции ---")
            for s in self._club.list_sections():
                print(s.get_info())
        elif choice == "11":
            print("\n--- Записи ---")
            for e in self._enrollments.list_enrollments():
                print(e.get_info())
        elif choice == "12":
            eid = read_int("id записи: ")
            status = read_str("новый статус (active/paused/completed): ")
            e = self._enrollments.set_status(eid, status)
            print(f"Запись #{e.id}: статус → {e.status}")
        elif choice == "13":
            print("\n--- Загрузка секций ---")
            for line in self._reports.load_report():
                print(line)
        elif choice == "14":
            print("\n--- Свободные места ---")
            for line in self._reports.free_slots():
                print(line)
        elif choice == "15":
            print(f"\nДоход клуба: {self._reports.revenue():.2f} руб./мес")
        elif choice == "16":
            print("\n--- Возрастные группы ---")
            for group, count in self._reports.age_groups().items():
                print(f"{group:>5}: {count}")
        elif choice == "17":
            print("\n--- Спортсмены без секций ---")
            lines = self._reports.athletes_without_sections()
            print("\n".join(lines) if lines else "Все записаны.")
        elif choice == "18":
            path = self._reports.export_report()
            print(f"Отчёт сохранён: {path}")
        else:
            print("Такого пункта нет.")
        return True

    def _add_coach(self) -> None:
        cid = read_int("id тренера: ")
        name = read_str("ФИО: ")
        age = read_int("возраст: ", min_value=1)
        phone = read_str("телефон: ")
        spec = read_str("специализация: ")
        exp = read_int("стаж: ")
        self._club.add_coach(Coach(cid, name, age, phone, spec, exp))
        print("Тренер добавлен.")

    def _add_athlete(self) -> None:
        aid = read_int("id спортсмена: ")
        name = read_str("ФИО: ")
        age = read_int("возраст: ", min_value=1)
        phone = read_str("телефон: ")
        cat = read_str("разряд: ")
        self._club.add_athlete(Athlete(aid, name, age, phone, cat))
        print("Спортсмен добавлен.")

    def _add_section(self) -> None:
        sid = read_int("id секции: ")
        name = read_str("название секции: ")
        sport = read_str("вид спорта: ")
        coach_id = read_int("id тренера: ")
        max_size = read_int("макс. участников: ", min_value=1)
        min_age = read_int("мин. возраст: ", min_value=0)
        self._club.add_section(
            Section(sid, name, sport, coach_id, max_size, min_age)
        )
        print("Секция добавлена.")

    def _enroll(self) -> None:
        aid = read_int("id спортсмена: ")
        sid = read_int("id секции: ")
        fee = read_float("абонплата в месяц: ")
        e: Enrollment = self._enrollments.enroll(aid, sid, fee)
        section = self._club.get_section(sid)
        athlete = self._club.get_athlete(aid)
        print(
            f"{athlete.name} записан(а) в '{section.name}', "
            f"запись #{e.id}."
        )