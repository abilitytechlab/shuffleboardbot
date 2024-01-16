from abc import ABC, abstractmethod

from controller.sjoel_controller_gcode import SjoelControllerGcode


class SjoelServerAbc(ABC):
    def __init__(self, controller: SjoelControllerGcode):
        self.controller = controller

    @abstractmethod
    def init(self):
        """
        Starts the server
        """
        pass
