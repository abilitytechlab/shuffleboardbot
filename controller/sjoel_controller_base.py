import enum
from abc import ABC, abstractmethod

from settings.device_settings import DeviceSettings


class MovementDirection(enum.Enum):
    """
    An enum for the direction of movement
    """
    LEFT = 1
    RIGHT = 0


class SjoelControllerBase(ABC):
    def __init__(self, settings: DeviceSettings):
        """
        A class that controls a sjoelbak
        :argument settings: The settings of the sjoelbak
        """
        self.settings = settings

    @abstractmethod
    def fire(self):
        """
        Fire the sjoelbak
        """
        pass

    @abstractmethod
    def move(self, direction: MovementDirection):
        """
        Move the sjoelbak
        :param direction: The direction to move the sjoelbak in
        :return: The position of the sjoelbak
        """
        pass

    @abstractmethod
    def start_move(self, direction: MovementDirection):
        """
        Start moving in a certain direction.
        Will keep moving until stop_move is called.
        """
        pass

    @abstractmethod
    def stop_move(self):
        """
        Stops moving
        """
        pass
