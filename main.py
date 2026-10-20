"""Консольный интерфейс для работы со спортивным клубом."""
from __future__ import annotations
from models import (Coach, Athlete, Section,
                    SportsClubError, NotFoundError,
                    DuplicateError, ValidationError, SectionFullError)
from club import SportsClub


def read_int(prompt: str, min_value: int = 0) -> int:
    """Читает целое число с консоли, не меньше min_value."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Ошибка: нужно целое число. Попробуйте ещё раз.")
            continue
        if value < min_value:
            print(f"Ошибка: значение должно быть не меньше {min_value}.")
            continue
        return value


def read_str(prompt: str) -> str:
    """Читает непустую строку с консоли."""
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Поле не может быть пустым.")


def autosave(club: SportsClub) -> None:
    """Автосохранение в JSON и XML после каждого изменения."""
    try:
        club.save_to_json("club.json")
        club.save_to_xml("club.xml")
        print("(автосохранение выполнено)")
    except PermissionError:
        print("Предупреждение: нет доступа к файлу.")
    except OSError as e:
        print(f"Предупреждение: не удалось сохранить ({e}).")


def menu() -> None:
    """Главное меню программы."""
    club = SportsClub("Олимп")

    answer = input("Загрузить предыдущие данные из файла? (y/n): ").strip().lower()

    if answer == "y":
        loaded = False
        try:
            club.load_from_json("club.json")
            print("Данные загружены из club.json")
            loaded = True
        except FileNotFoundError:
            print("club.json не найден, пробуем club.xml...")
        except Exception as e:
            print(f"Не удалось загрузить club.json ({e})")

        if not loaded:
            try:
                club.load_from_xml("club.xml")
                print("Данные загружены из club.xml")
                loaded = True
            except FileNotFoundError:
                print("club.xml тоже не найден.")
            except Exception as e:
                print(f"Не удалось загрузить club.xml ({e})")

        if not loaded:
            print("Предыдущих данных нет, начинаем с пустого клуба.")
    else:
        print("Начинаем с пустого клуба.")

    autosave(club)

    while True:
        print(f"\nСпортивный клуб {club._name}")
        print("1. Добавить тренера")
        print("2. Добавить спортсмена")
        print("3. Добавить секцию")
        print("4. Записать спортсмена в секцию")
        print("5. Удалить тренера")
        print("6. Удалить спортсмена")
        print("7. Удалить секцию")
        print("8. Загрузить из JSON")
        print("9. Загрузить из XML")
        print("10. Показать всю информацию")
        print("0. Выход")

        choice = input("Выбор: ").strip()

        try:
            if choice == "1":
                cid = read_int("id тренера: ")
                name = read_str("ФИО: ")
                age = read_int("возраст: ")
                phone = read_str("телефон: ")
                spec = read_str("специализация: ")
                exp = read_int("стаж: ")
                club.add_coach(Coach(cid, name, age, phone, spec, exp))
                print("Тренер добавлен.")
                autosave(club)

            elif choice == "2":
                aid = read_int("id спортсмена: ")
                name = read_str("ФИО: ")
                age = read_int("возраст: ")
                phone = read_str("телефон: ")
                cat = read_str("разряд: ")
                club.add_athlete(Athlete(aid, name, age, phone, cat))
                print("Спортсмен добавлен.")
                autosave(club)

            elif choice == "3":
                sid = read_int("id секции: ")
                name = read_str("название секции: ")
                sport = read_str("вид спорта: ")
                coach_id = read_int("id тренера: ")
                club.get_coach(coach_id)          # проверка сразу
                max_size = read_int("макс. участников: ", min_value=1)
                club.add_section(Section(sid, name, sport, coach_id, max_size))
                print("Секция добавлена.")
                autosave(club)

            elif choice == "4":
                sid = read_int("id секции: ")
                aid = read_int("id спортсмена: ")
                club.enroll_athlete(sid, aid)
                section = club.get_section(sid)
                athlete = club.get_athlete(aid)
                print(f"{athlete.get_name()} записан(а) в '{section.get_name()}'.")
                autosave(club)

            elif choice == "5":
                cid = read_int("id тренера для удаления: ")
                club.delete_coach(cid)
                print(f"Тренер #{cid} удалён.")
                autosave(club)

            elif choice == "6":
                aid = read_int("id спортсмена для удаления: ")
                club.delete_athlete(aid)
                print(f"Спортсмен #{aid} удалён.")
                autosave(club)

            elif choice == "7":
                sid = read_int("id секции для удаления: ")
                club.delete_section(sid)
                print(f"Секция #{sid} удалена.")
                autosave(club)

            elif choice == "8":
                club.load_from_json("club.json")
                print("Загружено из club.json")

            elif choice == "9":
                club.load_from_xml("club.xml")
                print("Загружено из club.xml")

            elif choice == "10":
                print("\n--- Тренеры ---")
                for c in club._coaches.values():
                    print(c.get_info())
                print("--- Спортсмены ---")
                for a in club._athletes.values():
                    print(a.get_info())
                print("--- Секции ---")
                for s in club._sections.values():
                    print(s.get_info())

            elif choice == "0":
                print("До свидания!")
                break

            else:
                print("Такого пункта нет.")

        except ValidationError as e:
            print(f"Ошибка валидации: {e}")
        except DuplicateError as e:
            print(f"Дубликат: {e}")
        except NotFoundError as e:
            print(f"Не найдено: {e}")
        except SectionFullError as e:
            print(f"Секция переполнена: {e}")
        except SportsClubError as e:
            print(f"Ошибка клуба: {e}")
        except FileNotFoundError:
            print("Файл не найден. Сначала сохраните данные.")
        except PermissionError:
            print("Нет доступа к файлу.")
        except (KeyError, TypeError, ValueError) as e:
            print(f"Некорректные данные: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nПрерывание с клавиатуры. Выход.")