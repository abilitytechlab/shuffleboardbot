import toml


class DeviceSettings:
    def __init__(self,
                 port: str,
                 baudrate: int,
                 fire_servo_range: tuple[int, int],
                 stepper_range: tuple[int, int],
                 fire_delay: float,
                 fire_servo_name: str,
                 stepper_axis: str,
                 stepper_step: int):
        """
        Settings for the sjoelbak
        :param port: The COM port the sjoelbak is connected to
        :param baudrate: The baudrate of the serial connection
        :param fire_servo_range: Between which angles the servo should move to fire. Servo rests on the first position
        :param stepper_range: The range of the stepper motor (min, max)
        :param fire_delay: How long to keep the firing servo on the second angle
        :param fire_servo_name: Internal name of the firing servo
        :param stepper_axis: The axis to move the stepper motor on
        :param stepper_step: The amount of steps the stepper motor moves
        """
        self.port = port
        self.baudrate = baudrate
        self.fire_servo_range = fire_servo_range
        self.stepper_range = stepper_range
        self.fire_delay = fire_delay
        self.fire_servo_name = fire_servo_name
        self.stepper_axis = stepper_axis
        self.stepper_step = stepper_step

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
        return cls(**data)

    def __str__(self):
        return self.to_toml()
