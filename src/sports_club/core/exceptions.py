"""Исключения предметной области."""


class SportsClubError(Exception):
    """Базовое исключение для всех ошибок спортивного клуба."""


class NotFoundError(SportsClubError):
    """Сущность с указанным id не найдена."""


class DuplicateError(SportsClubError):
    """Попытка добавить сущность с уже существующим id."""


class SectionFullError(SportsClubError):
    """Попытка записать спортсмена в заполненную секцию."""


class ValidationError(SportsClubError):
    """Некорректные данные при создании объекта."""


class StorageError(SportsClubError):
    """Ошибка чтения/записи файла данных."""