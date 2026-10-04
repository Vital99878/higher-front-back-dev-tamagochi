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
    """Реализация игровой логики и управления ресурсами."""

    def rest_tamagochi(self) -> None:
        """
        Дать питомцу отдохнуть.

        :return: None
        """
        self.tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """
        Поиграть с питомцем.

        :return: None
        """
        self.tamagochi.play()

    def heal_tamagochi(self) -> None:
        """
        Вылечить питомца первым доступным лекарством из инвентаря.

        После последнего использования лекарство удаляется из инвентаря.

        :return: None
        :raises ValueError: если в инвентаре нет лекарств
        """
        if not self._medicine:
            raise ValueError("Нет лекарства")

        medicine = self._medicine[0]
        self.tamagochi.heal(medicine)

        if medicine.is_empty():
            self._medicine.pop(0)

    def feed_tamagochi(self) -> None:
        """
        Покормить питомца первой доступной едой из инвентаря.

        Еда удаляется из инвентаря после успешного кормления.

        :return: None
        :raises ValueError: если в инвентаре нет еды
        """
        if not self._food:
            raise ValueError("Еды нету")

        food = self._food[0]
        self.tamagochi.feed(food)
        self._food.pop(0)

    def buy_medicine(self) -> None:
        """
        Купить самое дешёвое доступное лекарство.

        Для каждой покупки создаётся новый экземпляр Medicine, чтобы
        количество использований каждой упаковки хранилось независимо.

        :return: None
        :raises NotEnoughMoney: если монет недостаточно для покупки
        """
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
        """
        Купить самый дешёвый доступный продукт.

        :return: None
        :raises NotEnoughMoney: если монет недостаточно для покупки
        """
        food = min(
            self._all_food,
            key=lambda item: item.price,
        )

        if self._coins < food.price:
            raise NotEnoughMoney("Недостаточно монет")

        self._coins -= food.price
        self._food.append(food)

    def work(self) -> int:
        """
        Выполнить действие «работа» и увеличить баланс монет.

        :return: количество монет, заработанных за текущее действие
        """
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
        """
        Инициализировать игровое состояние.

        :param tamagochi: экземпляр питомца, реализующий AbstractTamagochi
        :param clicker: экземпляр кликера, реализующий AbstractClicker
        :param all_food: каталог доступной еды
        :param all_medicine: каталог доступных лекарств
        :return: None
        """
        self.tamagochi = tamagochi
        self._clicker = clicker

        self._all_food = all_food.copy()
        self._all_medicine = all_medicine.copy()

        self._food: list[Food] = []
        self._medicine: list[Medicine] = []

        self._coins = 0

    @property
    def food(self) -> list[Food]:
        """
        Получить список купленной еды.

        Возвращается копия списка, чтобы внешний код не мог напрямую
        изменить внутренний инвентарь игры.

        :return: копия списка объектов Food в инвентаре
        """
        return self._food.copy()

    @property
    def medicine(self) -> list[Medicine]:
        """
        Получить список купленных лекарств.

        Возвращается копия списка, чтобы внешний код не мог напрямую
        изменить структуру внутреннего инвентаря игры.

        :return: копия списка объектов Medicine в инвентаре
        """
        return self._medicine.copy()

    def get_status(self) -> dict[str, Any]:
        """
        Получить объединённый статус питомца и игры.

        :return: словарь с характеристиками питомца и количеством монет
        """
        return {
            **self.tamagochi.status,
            'coins': self._coins,
        }
