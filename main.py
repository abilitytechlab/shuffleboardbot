import argparse

from serial import SerialException

from communicator.communicator_mock import MockCommunicator
from server.sjoel_server_socket import SjoelServerSocket
from settings import HostingSettings
from sjoel_controller import SjoelController
from server.sjoel_server_simple import SjoelServerSimple


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


if __name__ == '__main__':
    # load settings
    hosting_settings = parse_hosting_settings()

    if hosting_settings.debug:
        print("Debug logging enabled")
        print("Hosting settings:")
        print(hosting_settings)

    try:
        device_settings = hosting_settings.get_device_settings()
    except FileNotFoundError:
        print("Config file not found")
        exit(1)

    if hosting_settings.debug:
        print("Device settings:")
        print(device_settings)

    # process overrides
    if hosting_settings.serial is not None:
        device_settings.serial_port = hosting_settings.serial

    if hosting_settings.baud is not None:
        device_settings.baud_rate = hosting_settings.baud

    # create controller
    communicator = None
    if hosting_settings.mock:
        communicator = MockCommunicator()

    try:
        controller = SjoelController(device_settings, communicator)
    except SerialException as e:
        print(e)
        exit(1)

    web = SjoelServerSocket(hosting_settings, controller)
    web.run()
