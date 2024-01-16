import time
from typing import Literal

import helpers
from communicator.communicator_abc import CommunicatorAbc
from communicator.communicator_serial import SerialCommunicator
from settings import DeviceSettings


class SjoelController:
    def __init__(self, settings: DeviceSettings, communicator: CommunicatorAbc = None):
        """
        A class that controls a sjoelbak
        :argument settings: The settings of the sjoelbak
        """
        self.settings = settings
        self.fire_servo_angle = self.settings.fire_servo_range[0]

        if communicator is None:
            communicator = SerialCommunicator(self.settings.port, self.settings.baudrate)

        self.communicator = communicator
        self._set_fire_servo_angle(self.fire_servo_angle)
        self.stepper_pos = 0  # Initialize stepper position
        self.communicator.write_command("M92 X1000")  # steps per mm


    def _set_stepper_active(self, active: bool):
        command = "M17" if active else "M18"
        self.communicator.write_command(command)

    def _set_fire_servo_angle(self, angle: int):
        """
        Set the angle of the firing servo
        :param angle: The angle to set the servo to
        """
        self.fire_servo_angle = angle
        self.communicator.write_command(f"M280 {self.settings.fire_servo_name} S{self.fire_servo_angle}")


    def _set_stepper_pos(self, pos: int):
        """
        Set the position of the stepper motor
        :param pos: The position to set the stepper motor to
        """
        unclamped_pos = self.stepper_pos
        self.stepper_pos = helpers.clamp_range(pos, self.settings.stepper_range)
        if self.stepper_pos == unclamped_pos:
            return

        self._set_stepper_active(True)
        # G0 is the move command, F is the speed
        self.communicator.write_command(f"G0 {self.settings.stepper_axis}{self.stepper_pos} F2000")
        self._set_stepper_active(False)

    def _can_fire(self):
        """
        Check if the sjoelbak can fire
        """
        return self.fire_servo_angle == self.settings.fire_servo_range[0]

    def fire(self):
        """
        Fire the sjoelbak, first turns on the fan
        which turns on the firing motors via a relay
        """
        if not self._can_fire():
            raise RuntimeError("Cannot fire while firing")
        self.communicator.write_command("M106 S255")
        self._set_fire_servo_angle(self.settings.fire_servo_range[1])
        time.sleep(self.settings.fire_delay)
        self._set_fire_servo_angle(self.settings.fire_servo_range[0])
        self.communicator.write_command("M106 S0")

    def move_raw(self, steps: int) -> int:
        """
        Move the stepper motor a certain amount of steps from the current position
        :param steps: The amount of steps to move the stepper motor
        """
        self._set_stepper_pos(self.stepper_pos + steps)
        return self.stepper_pos

    def move(self, direction: Literal["left", "right"]) -> int:
        """
        Move the stepper motor in a certain direction
        :param direction: The direction to move the stepper motor in
        """
        if direction == "left":
            self.move_raw(-self.settings.stepper_step)
        elif direction == "right":
            self.move_raw(self.settings.stepper_step)
        else:
            raise ValueError("Invalid direction")

        return self.stepper_pos

    def move_to(self, pos: int) -> int:
        """
        Move the stepper motor to a certain position
        :param pos: The position to move the stepper motor to
        """
        self._set_stepper_pos(pos)
        return self.stepper_pos

    def center(self) -> int:
        """
        Center the stepper motor
        """
        # self.move_to((self.settings.stepper_range[1] - self.settings.stepper_range[0]) // 2)
        self._set_stepper_active(True)
        self.communicator.write_command("G28")
        self._set_stepper_active(False)
        self.stepper_pos = 0
        return self.stepper_pos
