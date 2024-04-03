import enum
from abc import ABC, abstractmethod

from communicator.communicator_abc import CommunicatorText
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
