import time

from controller.sjoel_controller_base import MovementDirection
from settings.raw_controls_settings import RawControlsSettings
import pigpio


class CommunicatorRaw:
    def __init__(self, settings: RawControlsSettings):
        self.settings = settings

        self.pi = pigpio.pi()

        # Stepper
        self.pi.set_mode(self.settings.stepper_enable_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.settings.stepper_step_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.settings.stepper_dir_pin, pigpio.OUTPUT)
        self.delay = 0.005 / 4

        # Servo
        self.pi.set_mode(self.settings.servo_pin, pigpio.OUTPUT)

    def set_stepper_state(self, state: bool):
        """
        Set the state of the stepper motor.
        Sets the enable pin to the given state.
        """
        self.pi.write(self.settings.stepper_enable_pin, state)

    def move_stepper(self, direction: MovementDirection, steps: int):
        """
        Move the stepper motor.
        Moves the given amount of steps in the given direction.
        """
        # write direction
        direction_value = 1 if direction == MovementDirection.LEFT else 0
        self.pi.write(self.settings.stepper_dir_pin, direction_value)

        # write steps
        for _ in range(steps):
            self.pi.write(self.settings.stepper_step_pin, 1)
            time.sleep(self.delay)
            self.pi.write(self.settings.stepper_step_pin, 0)
            time.sleep(self.delay)
