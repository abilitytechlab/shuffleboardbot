import argparse

from serial import SerialException

from communicator.communicator_mock import MockCommunicator
from controller.sjoel_controller_gcode import SjoelControllerGcode
from hosting_settings import HostingSettings
from server.sjoel_server_socket import SjoelServerSocket


def parse_hosting_settings() -> HostingSettings:
    parser = argparse.ArgumentParser(description='Sjoeler 3000')
    parser.add_argument('--config', default='default.toml', help='Path to the config file, default: default.toml')
    parser.add_argument('--interface', default='0.0.0.0', type=str,
                        help='Override interface to listen on, default: 0.0.0.0')
    parser.add_argument('--port', default=5000, type=int, help='Override port to listen on, default: 5000')
    parser.add_argument('--serial', type=str, help='Override the serial port the robot is connected to')
    parser.add_argument('--baud', type=int, help='Override the baud rate of the serial connection')
    parser.add_argument('--debug', help='Enables debug logging', action='store_true')
    parser.add_argument('--mock', help='Enables the mock controller', action='store_true')
    args = parser.parse_args()

    return HostingSettings(args.config, args.interface, args.port, args.debug, args.mock, args.serial, args.baud)


def create_app(config: HostingSettings | None = None):
    # Load hosting settings if not provided
    if config is None:
        try:
            with open('config.toml') as f:
                config = HostingSettings.from_toml(f.read())
        except FileNotFoundError:
            print("Hosting settings not found")
            exit(1)

    # Load device settings
    try:
        device_settings = config.get_device_settings()
    except FileNotFoundError:
        print("Device settings not found")
        exit(1)

    communicator = None
    if config.mock:
        communicator = MockCommunicator()

    try:
        controller = SjoelControllerGcode(device_settings, communicator)
    except SerialException as e:
        print(e)
        exit(1)

    return SjoelServerSocket(controller).init()


if __name__ == '__main__':
    # load settings
    hosting_settings = parse_hosting_settings()
    web = create_app(hosting_settings)
    web.run(
        host=hosting_settings.interface,
        port=hosting_settings.port,
        debug=hosting_settings.debug)
