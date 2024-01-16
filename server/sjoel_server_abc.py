from abc import ABC, abstractmethod

from sjoel_controller import SjoelController


class SjoelServerAbc(ABC):
    def __init__(self, controller: SjoelController):
        self.controller = controller

    @abstractmethod
    def init(self):
        """
        Starts the server
        """
        pass
