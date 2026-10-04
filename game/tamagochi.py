"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from game.models import Food, Medicine

MAX_STATE_VALUE = 100
INITIAL_HP = 100
INITIAL_ENERGY = 100

FEED_ENERGY_COST = 2

PLAY_HUNGER_INCREASE = 5
PLAY_FATIGUE_INCREASE = 10
PLAY_ENERGY_COST = 10

REST_FATIGUE_RECOVERY = 10
REST_ENERGY_RECOVERY = 15
SICK_REST_DIVISOR = 2

TICK_HUNGER_INCREASE = 5
TICK_FATIGUE_INCREASE = 5
TICK_ENERGY_COST = 5

SICK_HUNGER_THRESHOLD = 80
SICK_FATIGUE_THRESHOLD = 80
SICK_ENERGY_THRESHOLD = 20

SICK_HP_LOSS = 10
SICK_FATIGUE_INCREASE = 5


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


class SimpleTamagochi(AbstractTamagochi):
    """Реализация питомца с изменяемыми игровыми характеристиками."""

    def feed(self, food: Food) -> None:
        """
        Накормить питомца.

        Уменьшает голод на значение сытости еды и немного расходует энергию.

        :param food: объект еды для кормления
        :return: None
        """
        self._hunger = max(0, self._hunger - food.satiety)
        self._energy = max(0, self._energy - FEED_ENERGY_COST)

    def play(self) -> None:
        """
        Поиграть с питомцем.

        Игра увеличивает голод и усталость и уменьшает запас энергии.

        :return: None
        """
        self._hunger = min(
            MAX_STATE_VALUE,
            self._hunger + PLAY_HUNGER_INCREASE,
        )
        self._fatigue = min(
            MAX_STATE_VALUE,
            self._fatigue + PLAY_FATIGUE_INCREASE,
        )
        self._energy = max(
            0,
            self._energy - PLAY_ENERGY_COST,
        )

    def rest(self) -> None:
        """
        Дать питомцу отдохнуть.

        Во время болезни отдых восстанавливает усталость и энергию
        менее эффективно.

        :return: None
        """
        fatigue_recovery = REST_FATIGUE_RECOVERY
        energy_recovery = REST_ENERGY_RECOVERY

        if self._sick:
            fatigue_recovery //= SICK_REST_DIVISOR
            energy_recovery //= SICK_REST_DIVISOR

        self._fatigue = max(0, self._fatigue - fatigue_recovery)
        self._energy = min(
            MAX_STATE_VALUE,
            self._energy + energy_recovery,
        )

    def heal(self, medicine: Medicine) -> None:
        """
        Вылечить питомца лекарством.

        Увеличивает здоровье, расходует одно использование лекарства
        и снимает состояние болезни.

        :param medicine: лекарство для лечения
        :return: None
        :raises ValueError: если лекарство закончилось
        """
        if medicine.is_empty():
            raise ValueError("Лекарство закончилось")

        self._hp += medicine.heal_hp
        medicine.uses += 1
        self._sick = False

    def update(self) -> None:
        """
        Обновить состояние питомца на один игровой тик.

        За тик увеличиваются голод и усталость и уменьшается энергия.
        При критических показателях питомец заболевает. Во время болезни
        уменьшается здоровье и дополнительно увеличивается усталость.

        :return: None
        """
        self._hunger = min(
            MAX_STATE_VALUE,
            self._hunger + TICK_HUNGER_INCREASE,
        )
        self._fatigue = min(
            MAX_STATE_VALUE,
            self._fatigue + TICK_FATIGUE_INCREASE,
        )
        self._energy = max(
            0,
            self._energy - TICK_ENERGY_COST,
        )

        if (
            self._hunger >= SICK_HUNGER_THRESHOLD
            or self._fatigue >= SICK_FATIGUE_THRESHOLD
            or self._energy <= SICK_ENERGY_THRESHOLD
        ):
            self._sick = True

        if self._sick:
            self._hp -= SICK_HP_LOSS
            self._fatigue = min(
                MAX_STATE_VALUE,
                self._fatigue + SICK_FATIGUE_INCREASE,
            )

    def __init__(self) -> None:
        """
        Инициализировать начальное состояние питомца.

        :return: None
        """
        self._hp = INITIAL_HP
        self._energy = INITIAL_ENERGY
        self._hunger = 0
        self._fatigue = 0
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """
        Получить текущее состояние питомца.

        :return: словарь с голодом, усталостью, здоровьем и энергией
        """
        return {
            "hunger": self._hunger,
            "fatigue": self._fatigue,
            "hp": self._hp,
            "energy": self._energy,
        }

    def is_alive(self) -> bool:
        """
        Проверить, жив ли питомец.

        :return: True, если здоровье не ниже нуля, иначе False
        """
        return self._hp >= 0

    def is_sick(self) -> bool:
        """
        Проверить, болеет ли питомец.

        :return: True, если питомец болеет, иначе False
        """
        return self._sick
