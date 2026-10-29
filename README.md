# Спортивный клуб «Олимп»



Консольное приложение на Python для управления спортивным клубом: тренеры, спортсмены, секции, записи и отчёты. Проект построен по слоистой архитектуре с чётким разделением ответственности: модели, репозитории, сервисы и консольный интерфейс живут в отдельных пакетах. 



Данные сохраняются в **JSON** и **XML**, каждая сущность — в своём файле. Все изменения логируются в `data/club.log`.





## Структура проекта



```text

.

├── pyproject.toml

├── uv.lock

├── README.md

├── .gitignore

├── data/                    # Данные приложения (не отслеживаются в git)

│   ├── club.log

│   ├── coaches.json / coaches.xml

│   ├── athletes.json / athletes.xml

│   ├── sections.json / sections.xml

│   ├── enrollments.json / enrollments.xml

│   └── reports/

└── src/

    └── sports_club/

        ├── __init__.py

        ├── main.py          # Точка входа (python -m sports_club)

        ├── app.py           # Composition root + запуск

        ├── core/

        │   ├── exceptions.py # SportsClubError и наследники

        │   ├── config.py     # Пути к файлам данных

        │   └── logging.py    # setup_logging()

        ├── models/

        │   ├── person.py     # Person, Coach, Athlete

        │   ├── section.py

        │   ├── enrollment.py

        │   └── serialization.py # Функции *_from_dict

        ├── repositories/

        │   ├── base.py       # BaseRepository[T]

        │   ├── coach_repository.py

        │   ├── athlete_repository.py

        │   ├── section_repository.py

        │   ├── enrollment_repository.py

        │   └── storage/

        │       ├── json_storage.py

        │       └── xml_storage.py

        ├── services/

        │   ├── club_service.py

        │   ├── enrollment_service.py

        │   └── report_service.py

        └── ui/

            └── console.py    # ConsoleApp

```



### Назначение модулей

| Пакет | Что содержит |
| :--- | :--- |
| `core` | Пользовательские исключения, пути (`config.py`), настройка `logging`. |
| `models` | Доменные классы `Person`, `Coach`, `Athlete`, `Section`, `Enrollment` и функции `*_from_dict`. Не содержат логики работы с файлами. |
| `repositories` | `BaseRepository[T]` с общим CRUD и по одному репозиторию на сущность. Персистентность реализована через `JsonStorage` и `XmlStorage`. |
| `services` | `ClubService` (CRUD + проверка ссылок), `EnrollmentService` (управление записями и статусами), `ReportService` (генерация отчётов и экспорт). |
| `ui` | `ConsoleApp` — меню, ввод/вывод данных, обработка исключений. Не работает с файлами и репозиториями напрямую. |
| `app.py` | Composition root: инициализирует репозитории, загружает данные, создаёт сервисы и передаёт их в `ConsoleApp`. Единственное место, где известны все слои. |



## Архитектура



Приложение спроектировано по принципам слоистой архитектуры. Зависимости направлены строго сверху вниз:



```text

ui → services → repositories → models → core

```



- `models` и `core` ничего не знают о слоях выше.

- `repositories` изолированы друг от друга.

- Связи между сущностями (тренер ↔ секция, спортсмен ↔ секция) обрабатываются **только в сервисах**.

- `ui` взаимодействует исключительно с сервисами и перехватывает `SportsClubError`.



**Пример цепочки вызовов при записи спортсмена в секцию:**

```text

ConsoleApp → EnrollmentService.enroll()

  → athletes.get(aid)                  # NotFoundError

  → sections.get(sid)                  # NotFoundError

  → проверка дубликата                 # DuplicateError

  → _active_count(sid) >= max_size     # SectionFullError

  → athlete.age < section.min_age      # ValidationError

  → enrollments.add(Enrollment(...))

  → JsonStorage.write + XmlStorage.write

```



---



## Установка и запуск



Убедитесь, что у вас установлен менеджер пакетов [uv](https://github.com/astral-sh/uv).



```bash

git clone <URL_репозитория>

cd <папка_проекта>

uv sync          # Создаст виртуальное окружение, установит пакет и зависимости

uv run sports-club

```



Альтернативный вариант запуска:

```bash

uv run python -m sports_club

```



Команда `sports-club` зарегистрирована автоматически благодаря блоку `[project.scripts]` в `pyproject.toml`:

```toml

[project.scripts]

sports-club = "sports_club.app:run"

```



---



## Как пользоваться



При старте приложение пытается загрузить данные из файлов `data/*.json` (если они отсутствуют — из `data/*.xml`). Если файлы не найдены, приложение инициализирует пустой клуб.



### Главное меню

```text

1. Добавить тренера

2. Добавить спортсмена

3. Добавить секцию

4. Записать спортсмена в секцию

5. Удалить тренера

6. Удалить спортсмена

7. Удалить секцию

8. Показать всех тренеров

9. Показать всех спортсменов

10. Показать все секции

11. Показать все записи

12. Сменить статус записи

13. Отчёт: загрузка секций

14. Отчёт: свободные места

15. Отчёт: доход клуба

16. Отчёт: возрастные группы

17. Спортсмены без секций

18. Экспортировать отчёт в файл

0. Выход

```



### Пример сеанса работы

```text

Спортивный клуб «Олимп»

Главное меню:

Выбор: 1

id тренера: 1

ФИО: Иванов Иван Иванович

возраст: 40

телефон: +7-900-000-00-00

специализация: Плавание

стаж: 15

Тренер добавлен.



Выбор: 3

id секции: 1

название секции: Плавание для начинающих

вид спорта: Плавание

id тренера: 1

макс. участников: 10

мин. возраст: 7

Секция добавлена.



Выбор: 4

id спортсмена: 1

id секции: 1

абонплата в месяц: 2500

Петров Пётр Петрович записан(а) в 'Плавание для начинающих', запись #1.



Выбор: 13

--- Загрузка секций ---

Плавание для начинающих              1/10  ( 10.0%)



Выбор: 15

Доход клуба: 2500.00 руб./мес



Выбор: 18

Отчёт сохранён: data/reports/report_20261028_153012.json

```



---



## Формат данных



Каждая сущность сохраняется в отдельном файле.



### `data/coaches.json`

```json

[

  {

    "id": 1,

    "name": "Иванов Иван Иванович",

    "age": 40,

    "phone": "+7-900-000-00-00",

    "specialization": "Плавание",

    "experience": 15

  }

]

```



### `data/sections.json`

```json

[

  {

    "id": 1,

    "name": "Плавание для начинающих",

    "sport": "Плавание",

    "coach_id": 1,

    "max_size": 10,

    "min_age": 7

  }

]

```



### `data/athletes.json`

```json

[

  {

    "id": 1,

    "name": "Петров Пётр Петрович",

    "age": 12,

    "phone": "+7-900-111-11-11",

    "category": "III"

  }

]

```



### `data/enrollments.json`

```json

[

  {

    "id": 1,

    "athlete_id": 1,

    "section_id": 1,

    "enrolled_at": "2026-10-28",

    "status": "active",

    "monthly_fee": 2500.0

  }

]

```



### `data/coaches.xml` (пример)

```xml

<?xml version="1.0" encoding="utf-8"?>

<coaches>

  <coach id="1">

    <name>Иванов Иван Иванович</name>

    <age>40</age>

    <phone>+7-900-000-00-00</phone>

    <specialization>Плавание</specialization>

    <experience>15</experience>

  </coach>

</coaches>

```



**Связи между сущностями:**

- `Section.coach_id` → `coaches.json[].id`

- `Enrollment.athlete_id` → `athletes.json[].id`

- `Enrollment.section_id` → `sections.json[].id`


---

| Исключение | Когда возникает |
| :--- | :--- |
| `ValidationError` | Передача некорректных данных (пустое ФИО, возраст вне диапазона 1–100, `max_size <= 0`, возраст спортсмена меньше `min_age`, битые внешние ссылки). |
| `DuplicateError` | Попытка создать сущность с существующим `id` или создать повторную активную запись в ту же секцию. |
| `NotFoundError` | Обращение к несуществующему тренеру, спортсмену или секции. |
| `SectionFull` / `SectionFullError` | Попытка записи в секцию, где уже достигнут лимит `max_size`. |
| `StorageError` | Ошибки чтения/записи файлов JSON/XML. |



## Особенности реализации





- **Атомарная запись в файл** 

- **Абсолютные импорты** от корня пакета (например, `from sports_club.models.person import Coach`).

- Строгая типизация (`type annotations`) для всех публичных методов.

- Активное использование декоратора `@property` вместо классических геттеров.

- **Полное отсутствие внешних зависимостей** — только стандартная библиотека Python.



---


ние REST API или Telegram-бота поверх существующих сервисов (слоистая архитектура позволяет это сделать без изменения бизнес-логики).