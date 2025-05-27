from pydantic import BaseModel


class RawControlsSettings(BaseModel):
    servo_pin: int
    servo_frequency: int
    servo_min_pulse: int
    servo_max_pulse: int
    servo_movement_delay: float

    stepper_enable_pin: int
    stepper_direction_pin: int
    stepper_step_pin: int
    stepper_frequency: int
    stepper_delay: float

    wheel_left_enable: int
    wheel_left_in1: int
    wheel_left_in2: int
    wheel_right_enable: int
    wheel_right_in1: int
    wheel_right_in2: int

    limitswitch_pin_left: int
    limitswitch_pin_right: int
