"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class Tamagochi(AbstractTamagochi):
    def feed(self, food: Food) -> None:
        # max - защита от < 0
        self._hunger = max(0, self._hunger - food.satiety)
        self._energy = max(0, self._energy - 2)

    def play(self) -> None:
        self._hunger += 5
        self._fatigue += 10
        self._energy = max(0, self._energy - 10)

    def rest(self) -> None:
        fatigue_recovery = 10
        energy_recovery = 15

        if self._sick:
            fatigue_recovery //= 2
            energy_recovery //= 2

        self._fatigue = max(0, self._fatigue - fatigue_recovery)
        self._energy = min(100, self._energy + energy_recovery)

    def heal(self, medicine: Medicine) -> None:
        if medicine.is_empty():
            raise ValueError("Лекарство закончилось")

        self._hp += medicine.heal_hp
        medicine.uses += 1

    def update(self) -> None:
        pass

    def __init__(self) -> None:
        self._hp = 100
        self._energy = 100
        self._hunger = 0
        self._fatigue = 0
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        return {
            "hunger": self._hunger,
            "fatigue": self._fatigue,
            "hp": self._hp,
            "energy": self._energy,
        }

    def is_alive(self) -> bool:
        return self._hp >= 0

    def is_sick(self) -> bool:
        return self._sick


tamagochi = Tamagochi()

# print(tamagochi.status)
# print(tamagochi.is_alive())
# print(tamagochi.is_sick())

# medicine = Medicine(
#     name="Ибупрофен",
#     price=30,
#     heal_hp=20,
#     number_of_uses=2,
# )
#
# tamagochi.heal(medicine)
# tamagochi.heal(medicine)
# tamagochi.heal(medicine)