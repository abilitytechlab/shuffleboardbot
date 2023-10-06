from abc import ABC, abstractmethod

from settings import HostingSettings
from sjoel_controller import SjoelController


class SjoelServerAbc(ABC):
    def __init__(self, settings: HostingSettings, controller: SjoelController):
        self.settings = settings
        self.controller = controller

    @abstractmethod
    def run(self):
        """
        Starts the server
        """
        pass
