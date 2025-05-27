import threading
import time

# import mygpio as pigpio
import pigpio

from controller.sjoel_controller_base import MovementDirection
from settings.raw_controls_settings import RawControlsSettings
from shutdown_helper import ShutdownHelper


class CommunicatorRaw:
    def __init__(self, settings: RawControlsSettings):
        self.shutdown_helper = ShutdownHelper(4 * 3600)
        self.settings = settings
        self.pi = pigpio.pi()
        self._last_direction = None
        self.motors_enabled = False

        # Stepper
        self.pi.set_mode(self.settings.stepper_enable_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.settings.stepper_step_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.settings.stepper_direction_pin, pigpio.OUTPUT)
        self.delay = 0.0005

        # Continuous stepper
        self._current_direction = None
        self._last_direction = None
        self._move_worker = threading.Thread(target=self._move, daemon=True)
        self._move_worker.start()

        # Servo
        self.pi.set_mode(self.settings.servo_pin, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.settings.servo_pin, self.settings.servo_frequency)
        self.servo_step_size = (self.settings.servo_max_pulse - self.settings.servo_min_pulse) / 180

        # Wheels left
        self.pi.set_mode(self.settings.wheel_left_in1, pigpio.OUTPUT)
        self.pi.set_mode(self.settings.wheel_left_in2, pigpio.OUTPUT)
        self.pi.write(self.settings.wheel_left_in1, 1)
        self.pi.write(self.settings.wheel_left_in2, 0)

        # Wheels right
        self.pi.set_mode(self.settings.wheel_right_in1, pigpio.OUTPUT)
        self.pi.set_mode(self.settings.wheel_right_in2, pigpio.OUTPUT)
        self.pi.write(self.settings.wheel_right_in2, 1)
        self.pi.write(self.settings.wheel_right_in1, 1)

        self.set_motor_enabled(True)

        # limit switch
        self.pi.set_mode(self.settings.limitswitch_pin_right, pigpio.INPUT)
        self.pi.set_mode(self.settings.limitswitch_pin_left, pigpio.INPUT)

    def set_stepper_state(self, state: bool):
        """
        Set the state of the stepper motor.
        Sets the enable pin to the given state.
        """
        self.shutdown_helper.update()
        self.pi.write(self.settings.stepper_enable_pin, state)

    def move_stepper(self, direction: MovementDirection):
        """
        Move the stepper motor.
        Moves the given amount of steps in the given direction.
        """
        self.shutdown_helper.update()
        self._current_direction = direction

    def set_servo_angle(self, angle: float):
        """
        Moves the servo to the given angle.
        """
        self.shutdown_helper.update()
        pulse_width = int(self.settings.servo_min_pulse + angle * self.servo_step_size)

        # Make sure the pulse width is within the allowed range
        if pulse_width < self.settings.servo_min_pulse:
            print(f"Warning: Servo pulse width {pulse_width} is below minimum {self.settings.servo_min_pulse}",
                  flush=True)
            pulse_width = self.settings.servo_min_pulse
        elif pulse_width > self.settings.servo_max_pulse:
            print(f"Warning: Servo pulse width {pulse_width} is above maximum {self.settings.servo_max_pulse}",
                  flush=True)
            pulse_width = self.settings.servo_max_pulse

        # Move the servo
        self._set_servo_pulsewidth(pulse_width)
        time.sleep(self.settings.servo_movement_delay)
        self._set_servo_pulsewidth(0)

    def _set_servo_pulsewidth(self, pulsewidth: int):
        """
        Sets the servo pulsewidth.
        """
        print(f"Setting servo pulse {pulsewidth}", flush=True)
        self.pi.set_servo_pulsewidth(self.settings.servo_pin, pulsewidth)

    def set_motor_enabled(self, enabled: bool):
        self.shutdown_helper.update()
        self.motors_enabled = enabled
        self.pi.write(self.settings.wheel_left_in1, 1 if enabled else 0)
        self.pi.write(self.settings.wheel_left_in2, 0)
        self.pi.write(self.settings.wheel_right_in1, 1 if enabled else 0)
        self.pi.write(self.settings.wheel_right_in2, 1 if enabled else 0)

    def start_move(self, direction: MovementDirection):
        self.shutdown_helper.update()
        self._current_direction = direction

    def stop_move(self):
        self.shutdown_helper.update()
        self._current_direction = None

    def _move(self):
        while True:
            limit_pin = self.settings.limitswitch_pin_right \
                if self._current_direction == MovementDirection.RIGHT \
                else self.settings.limitswitch_pin_left

            if self._current_direction is None or self.pi.read(limit_pin) == 1:
                self.pi.set_PWM_dutycycle(self.settings.stepper_step_pin, 0)
            elif self._current_direction != self._last_direction:
                direction_value = 0 if self._current_direction == MovementDirection.LEFT else 1
                self.pi.write(self.settings.stepper_direction_pin, direction_value)
                self.pi.set_PWM_frequency(self.settings.stepper_step_pin, self.settings.stepper_frequency)
                self.pi.set_PWM_dutycycle(self.settings.stepper_step_pin, 128)

            self._last_direction = self._current_direction
            time.sleep(0.1)

    def __del__(self):
        self.set_motor_enabled(False)
