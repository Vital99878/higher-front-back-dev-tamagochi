"""Модуль с интерфейсом и реализацией кликера."""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер со случайным количеством монет за один клик."""

    def __init__(self, min_income: int, max_income: int) -> None:
        """
        Инициализировать кликер с заданным диапазоном дохода.

        :param min_income: минимальное количество монет за клик
        :param max_income: максимальное количество монет за клик
        :return: None
        :raises ValueError: если диапазон дохода задан некорректно
        """
        if min_income < 0 or max_income < min_income:
            raise ValueError("Некорректный диапазон дохода")

        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = min_income

    @property
    def income_per_click(self) -> int:
        """
        Получить количество монет, выпавшее за последний клик.

        :return: количество монет за последний клик
        """
        return self._income_per_click

    def click(self) -> None:
        """
        Выполнить клик и определить случайный доход.

        :return: None
        """
        self._income_per_click = randint(
            self._min_income,
            self._max_income,
        )
