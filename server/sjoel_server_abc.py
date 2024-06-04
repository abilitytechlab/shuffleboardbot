from abc import ABC, abstractmethod

from controller.sjoel_controller_base import SjoelControllerBase


class SjoelServerAbc(ABC):
    def __init__(self, controller: SjoelControllerBase):
        self.controller = controller

    @abstractmethod
    def init(self):
        """
        Starts the server
        """
        pass
