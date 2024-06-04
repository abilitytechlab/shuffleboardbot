from pydantic import BaseModel


class GcodeSettings(BaseModel):
    port: str
    baudrate: int
    fire_servo_name: str
    stepper_axis: str
    stepper_step: int
    stepper_steps_per_mm: int
    stepper_rate: int
