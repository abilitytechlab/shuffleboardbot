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
        self.delay = 0.0005

        # Servo
        self.pi.set_mode(self.settings.servo_pin, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.settings.servo_pin, self.settings.servo_frequency)
        self.servo_step_size = (self.settings.servo_max_pulse - self.settings.servo_min_pulse) / 180
        # Limit
        self.pi.set_mode(self.settings.limit_pin, pigpio.INPUT)
        self.pi.set_pull_up_down(self.settings.limit_pin, pigpio.PUD_UP)
        self.pi.callback(self.settings.limit_pin, pigpio.RISING_EDGE, lambda gpio, level, tick: self._on_limit_pressed())
        self.pi.callback(self.settings.limit_pin, pigpio.FALLING_EDGE, lambda gpio, level, tick: self._on_limit_released())
        self._debounce_interval = 1 #ms
        self._last_trigger = 0
        self._is_locked = False
        self._locked_direction = None

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
        self._last_direction = direction
        print(f"moving {direction}")

        # write steps
        for _ in range(steps):
            # Check if we are allowed to move every step
            if not self._is_locked or direction is not self._locked_direction:
                self.pi.write(self.settings.stepper_step_pin, 1)
                time.sleep(self.delay)
                self.pi.write(self.settings.stepper_step_pin, 0)
                time.sleep(self.delay)
            else:
                return

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

    def _on_limit_pressed(self):
        # print why
        if ((time.time_ns() - self._last_trigger)/1_000_000):
            print(f"limit pressed, locked direction: {self._locked_direction}, last direction: {self._last_direction}")
            self._locked_direction = self._last_direction
            self._is_locked = True
            self._last_trigger = time.time_ns()
    
    def _on_limit_released(self):
        if ((time.time_ns() - self._last_trigger)/1_000_000):
            print("limit released")
            self._locked_direction = None
            self._is_locked = False
            self._last_trigger = time.time_ns()
