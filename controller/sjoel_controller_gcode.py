import time

from communicator.communicator_abc import CommunicatorText
from communicator.communicator_serial import SerialCommunicator
from controller.sjoel_controller_base import SjoelControllerBase, MovementDirection
from settings.device_settings import DeviceSettings


class SjoelControllerGcode(SjoelControllerBase):
    def __init__(self, settings: DeviceSettings, communicator: CommunicatorText):
        """
        A class that controls a sjoelbak
        :argument settings: The settings of the sjoelbak
        """
        super().__init__(settings)
        self.communicator = communicator

        # Set relative positioning
        self.communicator.write_command("G91")

        # Set servo to initial position
        self.fire_servo_angle = self.settings.fire_servo_range[0]
        self._set_fire_servo_angle(self.fire_servo_angle)

        # Set steps per mm
        self.communicator.write_command(f"M92 {self.settings.gcode.stepper_axis}{self.settings.gcode.stepper_steps_per_mm}")

        # Home the stepper
        self._center()

    def fire(self):
        print("fire")
        """
        Fire the sjoelbak, first turns on the fan
        which turns on the firing motors via a relay
        """
        if not self._can_fire():
            raise RuntimeError("Cannot fire while firing")
        self._set_fan_speed(255)
        self._set_fire_servo_angle(self.settings.fire_servo_range[1])
        time.sleep(self.settings.fire_delay)
        self._set_fire_servo_angle(self.settings.fire_servo_range[0])
        self._set_fan_speed(0)

    def move(self, direction: MovementDirection):
        """
        Move the stepper motor in a certain direction
        :param direction: The direction to move the stepper motor in
        """
        if direction == MovementDirection.LEFT:
            self._move_raw(-self.settings.gcode.stepper_step)
        elif direction == MovementDirection.RIGHT:
            self._move_raw(self.settings.gcode.stepper_step)
            # print("i should move to the right, it is calling right")
        else:
            raise ValueError("Invalid direction")

    def _set_stepper_active(self, active: bool):
        """
        Set the stepper motor active or inactive
        :param active: Whether the stepper motor should be active or not
        """
        command = "M17" if active else "M18"
        self.communicator.write_command(command)

    def _set_fire_servo_angle(self, angle: int):
        """
        Set the angle of the firing servo
        :param angle: The angle to set the servo to
        """
        self.fire_servo_angle = angle
        self.communicator.write_command(f"M280 {self.settings.gcode.fire_servo_name} S{self.fire_servo_angle}")

    def _set_fan_speed(self, speed: int):
        """
        Set the speed of the fan
        :param speed: The speed to set the fan to
        """
        self.communicator.write_command(f"M106 S{speed}")

    def _move_raw(self, steps: int):
        """
        Move the stepper motor a certain amount of steps from the current position
        :param steps: The amount of steps to move the stepper motor
        """
        self._set_stepper_active(True)
        self.communicator.write_command(f"G0 {self.settings.gcode.stepper_axis}{steps} F{self.settings.gcode.stepper_rate}")
        self._set_stepper_active(False)

    def _can_fire(self):
        """
        Check if the sjoelbak can fire
        """
        return self.fire_servo_angle == self.settings.fire_servo_range[0]

    def _center(self):
        """
        Center the stepper motor
        """
        self._set_stepper_active(True)
        self.communicator.write_command("G28")
        self._set_stepper_active(False)
