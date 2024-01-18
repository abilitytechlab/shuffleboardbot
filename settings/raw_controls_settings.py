from pydantic import BaseModel


class RawControlsSettings(BaseModel):
    servo_pin: int

    stepper_enable_pin: int
    stepper_direction_pin: int
    stepper_step_pin: int
