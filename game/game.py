"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from typing import Any

from .clicker import AbstractClicker
from .exceptions import NotEnoughMoney
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    def rest_tamagochi(self) -> None:
        self.tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        self.tamagochi.play()

    def heal_tamagochi(self) -> None:
        if not self._medicine:
            raise ValueError("Нет лекарства")

        medicine = self._medicine[0]

        self.tamagochi.heal(medicine)

        if medicine.is_empty():
            self._medicine.pop(0)

    def feed_tamagochi(self) -> None:
        if not self._food:
            raise ValueError("Еды нету")

        food = self._food.pop(0)
        self.tamagochi.feed(food)

    def buy_medicine(self) -> None:
        medicine = min(
            self._all_medicine,
            key=lambda item: item.price,
        )

        if self._coins < medicine.price:
            raise NotEnoughMoney("Недостаточно монет")

        self._coins -= medicine.price

        bought_medicine = Medicine(
            name=medicine.name,
            price=medicine.price,
            heal_hp=medicine.heal_hp,
            number_of_uses=medicine.number_of_uses,
        )

        self._medicine.append(bought_medicine)


    def buy_food(self) -> None:
        food = min(
            self._all_food,
            key=lambda item: item.price,
        )

        if self._coins < food.price:
            raise NotEnoughMoney("Недостаточно монет")

        self._coins -= food.price
        self._food.append(food)

    def work(self) -> int:
        self._clicker.click()

        income = self._clicker.income_per_click
        self._coins += income

        return income

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        self.tamagochi = tamagochi
        self._clicker = clicker

        self._all_food = all_food
        self._all_medicine = all_medicine

        self._food: list[Food] = []
        self._medicine: list[Medicine] = []

        self._coins = 0

    @property
    def food(self) -> list[Food]:
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        return self._medicine

    def get_status(self) -> dict[str, Any]:
        return {
            **self.tamagochi.status,
            'coins': self._coins,
        }
