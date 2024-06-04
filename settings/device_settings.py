import enum
from typing import Literal

import toml
from pydantic import BaseModel

from settings.gcode_settings import GcodeSettings
from settings.raw_controls_settings import RawControlsSettings


class CommunicatorType(enum.Enum):
    GCODE = "gcode"
    RAW = "raw"


class DeviceSettings(BaseModel):
    fire_servo_range: tuple[int, int]
    fire_delay: float
    stepper_range: tuple[int, int]
    communicator: CommunicatorType
    gcode: GcodeSettings | None = None
    raw: RawControlsSettings | None = None

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
