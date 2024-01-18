from communicator.communicator_raw import CommunicatorRaw
from controller.sjoel_controller_base import SjoelControllerBase, MovementDirection
from settings.device_settings import DeviceSettings


class SjoelControllerRaw(SjoelControllerBase):
    def __init__(self, settings: DeviceSettings, communicator: CommunicatorRaw):
        super().__init__(settings)
        self.communicator = communicator

    def fire(self):
        pass

    def move(self, direction: MovementDirection):
        pass