OUTPUT = 1
INPUT = 2


class pi:
    def __init__(self):
        self.modes = {}
        self.pwm_frequencies = {}
        self.pwm_dutycycles = {}
        self.servo_pulsewidths = {}
        self.states = {}

    def set_mode(self, pin, mode):
        self.modes[pin] = mode

    def get_mode(self, pin):
        return self.modes[pin]

    def set_PWM_frequency(self, pin, frequency):
        self.pwm_frequencies[pin] = frequency

    def get_PWM_frequency(self, pin):
        return self.pwm_frequencies[pin]

    def set_PWM_dutycycle(self, pin, dutycycle):
        self.pwm_dutycycles[pin] = dutycycle

    def get_PWM_dutycycle(self, pin):
        return self.pwm_dutycycles[pin]

    def set_servo_pulsewidth(self, pin, pulsewidth):
        self.servo_pulsewidths[pin] = pulsewidth

    def get_servo_pulsewidth(self, pin):
        return self.servo_pulsewidths[pin]

    def write(self, pin, value):
        self.states[pin] = value

    def read(self, pin):
        return self.states[pin]
