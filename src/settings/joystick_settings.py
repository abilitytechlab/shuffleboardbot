import enum

import toml
from pydantic import BaseModel


class PullDirection(enum.Enum):
    UP = "up"
    DOWN = "down"


class JoystickSettings(BaseModel):
    pin_button: int
    pin_left: int
    pin_right: int

    # Whether to pull the pins up or down.
    pull_direction: PullDirection

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

        return JoystickSettings(**data)

    def __str__(self):
        return self.to_toml()
