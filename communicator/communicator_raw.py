import time

import pigpio

from controller.sjoel_controller_base import MovementDirection
from settings.raw_controls_settings import RawControlsSettings


class CommunicatorRaw:
    def __init__(self, settings: RawControlsSettings):
        self.settings = settings

        self.pi = pigpio.pi()

        # Stepper
        self.pi.set_mode(self.settings.stepper_enable_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.settings.stepper_step_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.settings.stepper_direction_pin, pigpio.OUTPUT)
        self.delay = 0.005 / 4

        # Servo
        self.pi.set_mode(self.settings.servo_pin, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.settings.servo_pin, self.settings.servo_frequency)
        self.servo_step_size = (self.settings.servo_max_pulse - self.settings.servo_min_pulse) / 180

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
        self.pi.write(self.settings.stepper_direction_pin, direction_value)

        # write steps
        for _ in range(steps):
            self.pi.write(self.settings.stepper_step_pin, 1)
            time.sleep(self.delay)
            self.pi.write(self.settings.stepper_step_pin, 0)
            time.sleep(self.delay)

    def set_servo_angle(self, angle: float):
        """
        Moves the servo to the given angle.
        """
        pulse_width = int(self.settings.servo_min_pulse + angle * self.servo_step_size)

        # Make sure the pulse width is within the allowed range
        if pulse_width < self.settings.servo_min_pulse:
            print(f"Warning: Servo pulse width {pulse_width} is below minimum {self.settings.servo_min_pulse}")
            pulse_width = self.settings.servo_min_pulse
        elif pulse_width > self.settings.servo_max_pulse:
            print(f"Warning: Servo pulse width {pulse_width} is above maximum {self.settings.servo_max_pulse}")
            pulse_width = self.settings.servo_max_pulse

        # Move the servo
        self._set_servo_pulsewidth(pulse_width)
        time.sleep(self.settings.servo_movement_delay)
        self._set_servo_pulsewidth(0)

    def _set_servo_pulsewidth(self, pulsewidth: int):
        """
        Sets the servo pulsewidth.
        """
        self.pi.set_servo_pulsewidth(self.settings.servo_pin, pulsewidth)
