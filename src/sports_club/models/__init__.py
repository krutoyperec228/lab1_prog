"""Доменные модели спортивного клуба."""
from sports_club.models.person import Athlete, Coach, Person
from sports_club.models.section import Section
from sports_club.models.enrollment import Enrollment

__all__ = ["Person", "Coach", "Athlete", "Section", "Enrollment"]