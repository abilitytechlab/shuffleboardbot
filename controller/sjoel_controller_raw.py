import time

from communicator.communicator_raw import CommunicatorRaw
from controller.sjoel_controller_base import SjoelControllerBase, MovementDirection
from settings.device_settings import DeviceSettings


class SjoelControllerRaw(SjoelControllerBase):
    def __init__(self, settings: DeviceSettings, communicator: CommunicatorRaw):
        super().__init__(settings)
        self.communicator = communicator
        self.is_firing = False
        self.communicator.set_servo_angle(self.settings.fire_servo_range[0])

    def fire(self):
        if self.is_firing:
            return
        self.is_firing = True
        self.communicator.set_servo_angle(self.settings.fire_servo_range[1])
        time.sleep(self.settings.fire_delay)
        self.communicator.set_servo_angle(self.settings.fire_servo_range[0])
        self.is_firing = False

    def move(self, direction: MovementDirection):
        self.communicator.move_stepper(direction, self.settings.raw.stepper_steps)
