import argparse
import time

from communicator.communicator_mock import MockCommunicator
from communicator.communicator_serial import SerialCommunicator
from controller.sjoel_controller_gcode import SjoelControllerGcode
from joystick.sjoel_joystick_simple import SjoelJoystickSimple
from server.sjoel_server_socket import SjoelServerSocket
from settings.device_settings import CommunicatorType, DeviceSettings
from settings.hosting_settings import HostingSettings


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
            print("Hosting settings not found", flush=True)
            exit(1)

    # Load device settings
    try:
        device_settings = config.get_device_settings()
    except FileNotFoundError:
        print("Device settings not found", flush=True)
        exit(1)

    # Create controller
    if config.mock:
        print("Mock communicator enabled", flush=True)
        communicator = MockCommunicator()
        controller = SjoelControllerGcode(device_settings, communicator)
    else:
        if device_settings.communicator == CommunicatorType.GCODE:
            print("Gcode communicator enabled", flush=True)
            communicator = SerialCommunicator(device_settings.gcode.port, device_settings.gcode.baudrate)
            controller = SjoelControllerGcode(device_settings, communicator)
        elif device_settings.communicator == CommunicatorType.RAW:
            from communicator.communicator_raw import CommunicatorRaw
            from controller.sjoel_controller_raw import SjoelControllerRaw
            print("Raw communicator enabled", flush=True)
            communicator = CommunicatorRaw(device_settings.raw)
            controller = SjoelControllerRaw(device_settings, communicator)
        else:
            raise ValueError("Invalid communicator type")

    if device_settings.joystick is not None:
        print(f"Joystick enabled", flush=True)
        joystick = SjoelJoystickSimple(controller, device_settings.joystick)

    if device_settings.shutdown_pin is not None:
        import pigpio
        pi = pigpio.pi()
        pi.set_mode(device_settings.shutdown_pin, pigpio.INPUT)
        pi.set_pull_up_down(device_settings.shutdown_pin, pigpio.PUD_DOWN)
        pi.callback(device_settings.shutdown_pin, pigpio.RISING_EDGE, lambda: shutdown(device_settings))

    # Create server
    return SjoelServerSocket(controller).init()


def shutdown(device_settings: DeviceSettings):
    print("Shutting down", flush=True)

    import os
    os.system("shutdown -h now")

    if device_settings.shutdown_led_pin is not None:
        import pigpio
        pi = pigpio.pi()
        pi.set_mode(device_settings.shutdown_led_pin, pigpio.OUTPUT)
        while True:
            pi.write(device_settings.shutdown_led_pin, 1)
            time.sleep(0.1)
            pi.write(device_settings.shutdown_led_pin, 0)
            time.sleep(0.1)


if __name__ == '__main__':
    # load settings
    hosting_settings = parse_hosting_settings()
    web = create_app(hosting_settings)
    web.run(
        host=hosting_settings.interface,
        port=hosting_settings.port,
        debug=hosting_settings.debug)
