import enum
from abc import ABC, abstractmethod

from communicator.communicator_abc import CommunicatorAbc
from settings import DeviceSettings


class MovementDirection(enum.Enum):
    """
    An enum for the direction of movement
    """
    LEFT = 0
    RIGHT = 1


class SjoelControllerBase(ABC):
    def __init__(self, settings: DeviceSettings, communicator: CommunicatorAbc = None):
        """
        A class that controls a sjoelbak
        :argument settings: The settings of the sjoelbak
        """
        self.settings = settings
        self.communicator = communicator

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
