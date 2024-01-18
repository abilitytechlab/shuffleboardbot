import toml

from device_settings import DeviceSettings


class HostingSettings:
    def __init__(self,
                 config: str = 'default.toml',
                 interface: str = '0.0.0.0',
                 port: int = 5000,
                 debug: bool = False,
                 mock: bool = False,
                 serial: str | None = None,
                 baud: str | None = None) -> None:
        """
        Settings for the hosting of the webserver
        :param config: Path to the config file
        :param interface: Interface to listen on
        :param port: Port to listen on
        :param debug: Enables debug logging
        :param mock: Enables the mock controller
        :param serial: Override the serial port the robot is connected to
        :param baud: Override the baud rate of the serial connection
        """
        self.config = config
        self.debug = debug
        self.mock = mock
        self.serial = serial
        self.baud = baud
        self.interface = interface
        self.port = port

    def get_device_settings(self) -> DeviceSettings:
        """
        Get the device settings from the config file
        """
        with open(self.config, 'r') as config_file:
            return DeviceSettings.from_toml(config_file.read())

    @classmethod
    def from_toml(cls, toml_str):
        """
        Deserialize the settings from TOML format
        """
        data = toml.loads(toml_str)
        return cls(**data)

    def __str__(self):
        return toml.dumps(vars(self))
