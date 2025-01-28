import enum

import toml
from pydantic import BaseModel

from settings.gcode_settings import GcodeSettings
from settings.joystick_settings import JoystickSettings
from settings.raw_controls_settings import RawControlsSettings


class DeviceSettings(BaseModel):
    fire_servo_range: tuple[int, int]
    fire_delay: float
    stepper_range: tuple[int, int]
    shutdown_pin: int | None = None
    shutdown_led_pin: int | None = None
    raw: RawControlsSettings | None = None
    joystick: JoystickSettings | None = None

    def to_toml(self):
        """
        Serialize the settings to TOML format
        """
        return toml.dumps(vars(self))

    @classmethod
    def from_toml(cls, toml_str):
        """
        Deserialize the settings from TOML format
        """
        data = toml.loads(toml_str)

        return DeviceSettings(**data)

    def __str__(self):
        return self.to_toml()
