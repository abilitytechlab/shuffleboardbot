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
        self._move_worker = threading.Thread(target=self._move)
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

    def move_stepper(self, direction: MovementDirection, steps: int):
        """
        Move the stepper motor.
        Moves the given amount of steps in the given direction.
        """
        self.shutdown_helper.update()
        self._current_direction = direction
        self._move()

        # # write direction
        # direction_value = 1 if direction == MovementDirection.LEFT else 0
        # self.pi.write(self.settings.stepper_direction_pin, direction_value)
        # self._last_direction = direction
        # print(f"moving {direction}", flush=True)
        # limit_pin = self.settings.limitswitch_pin_right if direction == MovementDirection.RIGHT else self.settings.limitswitch_pin_left
        #
        # # write steps
        # for _ in range(steps):
        #     # Check if we are allowed to move every step
        #     if self.pi.read(limit_pin) == 0:
        #         print("move", flush=True)
        #         self.pi.write(self.settings.stepper_step_pin, 1)
        #         time.sleep(self.delay)
        #         self.pi.write(self.settings.stepper_step_pin, 0)
        #         time.sleep(self.delay)
        #     else:
        #         print("stop", flush=True)
        #         return

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
        if self._current_direction is not None:
            direction_value = 1 if self._current_direction == MovementDirection.LEFT else 0
            self.pi.write(self.settings.stepper_direction_pin, direction_value)

        self.pi.set_PWM_frequency(self.settings.stepper_step_pin, 500)
        self.pi.set_PWM_dutycycle(self.settings.stepper_step_pin, 128)
        time.sleep(1)
        self.pi.set_PWM_dutycycle(self.settings.stepper_step_pin, 0)

        # while True:
        #
        #
        #         # step
        #         print(f'moving in {last_dir}')
        #         self.pi.write(self.settings.stepper_step_pin, 1)
        #         time.sleep(self.delay)
        #         self.pi.write(self.settings.stepper_step_pin, 0)
        #         time.sleep(self.delay)
        #     else:
        #         time.sleep(0.1)

    def __del__(self):
        self.set_motor_enabled(False)
