import pigpio

from controller.sjoel_controller_base import SjoelControllerBase, MovementDirection
from settings.joystick_settings import JoystickSettings, PullDirection


class SjoelJoystickSimple:
    def __init__(self, controller: SjoelControllerBase, settings: JoystickSettings):
        self.controller = controller
        self.pi = pigpio.pi()

        pull_mode = pigpio.PUD_UP if settings.pull_direction == PullDirection.UP else pigpio.PUD_DOWN
        self.pi.set_pull_up_down(settings.pin_button, pull_mode)
        self.pi.set_pull_up_down(settings.pin_left, pull_mode)
        self.pi.set_pull_up_down(settings.pin_right, pull_mode)

        self.pi.set_mode(settings.pin_button, pigpio.INPUT)
        self.pi.set_mode(settings.pin_left, pigpio.INPUT)
        self.pi.set_mode(settings.pin_right, pigpio.INPUT)

        self.pi.callback(settings.pin_button, pigpio.EITHER_EDGE, self.button_callback)
        self.pi.callback(settings.pin_left, pigpio.EITHER_EDGE, self.left_callback)
        self.pi.callback(settings.pin_right, pigpio.EITHER_EDGE, self.right_callback)

    def button_callback(self, gpio, level, tick):
        print(f"Gpio {gpio}, level {level}, tick {tick}, button", flush=True)
        if level == 0:
            self.controller.fire()

    def left_callback(self, gpio, level, tick):
        print(f"Gpio {gpio}, level {level}, tick {tick}, left", flush=True)
        if level == 0:
            self.controller.move(MovementDirection.LEFT)

    def right_callback(self, gpio, level, tick):
        print(f"Gpio {gpio}, level {level}, tick {tick}, right", flush=True)
        if level == 0:
            self.controller.move(MovementDirection.RIGHT)

    def close(self):
        self.pi.stop()
