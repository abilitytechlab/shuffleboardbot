import threading
import time

from communicator.communicator_raw import CommunicatorRaw
from controller.sjoel_controller_base import SjoelControllerBase, MovementDirection
from settings.device_settings import DeviceSettings


class SjoelControllerRaw(SjoelControllerBase):
    def start_move(self, direction: MovementDirection):
        self.communicator.start_move(direction)

    def stop_move(self):
        self.communicator.stop_move()

    def __init__(self, settings: DeviceSettings, communicator: CommunicatorRaw):
        super().__init__(settings)
        self.communicator = communicator
        self.is_firing = False
        self.communicator.set_servo_angle(self.settings.fire_servo_range[0])
        self.last_fire = time.time()
        self.try_stop_thread = threading.Thread(target=self.try_stop_wheels)

    def fire(self):
        if self.is_firing:
            print("Cannot fire while firing", flush=True)
            return

        self.is_firing = True
        self.last_fire = time.time()

        # Make sure motors are started
        if not self.communicator.motors_enabled:
            print("Enabling motors", flush=True)
            self.communicator.set_motor_enabled(True)
            time.sleep(2)

        self.communicator.set_servo_angle(self.settings.fire_servo_range[1])
        time.sleep(self.settings.fire_delay)
        self.communicator.set_servo_angle(self.settings.fire_servo_range[0])

        self.is_firing = False

    def move(self, direction: MovementDirection):
        self.communicator.move_stepper(direction, self.settings.raw.stepper_steps)

    def try_stop_wheels(self):
        while True:
            if time.time() - self.last_fire > 15:
                print("No firing activity for 15 seconds, stopping motors", flush=True)
                self.communicator.set_motor_enabled(False)
            time.sleep(1)
