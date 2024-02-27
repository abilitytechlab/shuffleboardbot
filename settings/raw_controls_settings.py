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
    stepper_steps: int
