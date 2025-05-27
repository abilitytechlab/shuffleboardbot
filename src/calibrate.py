import time

import pigpio

from settings.hosting_settings import HostingSettings


def set_servo_angle(pi: pigpio, pin: int, angle: float, min_pulse: float = 1000, max_pulse: float = 2000):
    """
    Moves the servo to the given angle.
    """
    step_size = (max_pulse - min_pulse) / 180
    pulse_width = int(min_pulse + angle * step_size)

    # Make sure the pulse width is within the allowed range
    if pulse_width < min_pulse:
        print(f"Warning: Servo pulse width {pulse_width} is below minimum {min_pulse}",
              flush=True)
        pulse_width = min_pulse
    elif pulse_width > max_pulse:
        print(f"Warning: Servo pulse width {pulse_width} is above maximum {max_pulse}",
              flush=True)
        pulse_width = max_pulse

    # Move the servo
    pi.set_servo_pulsewidth(pin, pulse_width)

if __name__ == '__main__':
    try:
        with open('config.toml') as f:
            config = HostingSettings.from_toml(f.read())
    except FileNotFoundError:
        print("Hosting settings not found", flush=True)
        exit(1)

    try:
        device_settings = config.get_device_settings()
    except FileNotFoundError:
        print("Device settings not found", flush=True)
        exit(1)

    pi = pigpio.pi()

    angle = 90
    min_pulse = 1000
    max_pulse = 2000

    while True:
        angle_str = input(f"Angle ({angle})? ")
        min_pulse_str = input(f"Min pulse ({min_pulse})? ")
        max_pulse_str = input(f"Max pulse ({max_pulse})? ")

        angle = angle if angle_str == "" else float(angle_str)
        min_pulse = min_pulse if min_pulse_str == "" else float(min_pulse_str)
        max_pulse = max_pulse if max_pulse_str == "" else float(max_pulse_str)

        set_servo_angle(pi, device_settings.raw.servo_pin, angle, min_pulse, max_pulse)

