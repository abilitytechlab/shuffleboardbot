# SjoelFlask

Simple web application to control a sjoel robot with serial commands.

## Installation

1. `pip install -r requirements.txt`
2. ```
   python main.py [-h] [--config CONFIG] [--interface INTERFACE] [--port PORT] [--serial SERIAL] [--baud BAUD] [--debug] [--mock]
   
   options:
     -h, --help            show this help message and exit
     --config CONFIG       Path to the config file, default: default.toml
     --interface INTERFACE Override interface to listen on, default: 0.0.0.0
     --port PORT           Override port to listen on, default: 5000
     --serial SERIAL       Override the serial port the robot is connected to
     --baud BAUD           Override the baud rate of the serial connection
     --debug               Enables debug logging
     --mock                Enables the mock controller
   ```
   1. `python main.py --mock` to get up and running quickly without a robot connected
3. Open `http://localhost:5000` in your browser

## Configuration

We use a TOML file for the configuration of the device parameters.
The default configuration is as follows:

```toml
port = "COM3"                   # Serial port to connect to
baudrate = 9600                 # Baudrate of the serial connection
fire_servo_range = [120, 180]   # Range of the servo in degrees, first position is where it will rest
stepper_range = [0, 100]        # Range of the stepper in steps, default position is center
fire_delay = 1.0                # How long to keep the firing servo in the second position
fire_servo_name = "P0"          # Name of the servo that fires the puck
stepper_name = "G0"             # Name of the stepper that moves laterally
stepper_axis = "X"              # Axis of the stepper
stepper_step = 10               # How many steps to move the stepper per command
```

## Commands

Currently the software only communicates through GCode commands over a serial connection.

When the servo is fired, the software will send the following commands to the robot:

1. `M280 [servo_name] S[fire_servo_range[1]]`, e.g. `M280 P0 S180`
2. wait for `fire_delay` seconds
3. `M280 [servo_name] S[fire_servo_range[0]]`, e.g. `M280 P0 S120`

When the stepper is moved, the software will send the following commands to the robot:

1. `[stepper_name] [stepper_axis][position]`, e.g. `G0 X10`

## Todo

- [ ] Apparently `G0` is the command for moving the stepper, I assumed it was the stepper name, needs to be removed.
- [ ] Add a way to configure the commands that are sent
- [ ] Read position before moving stepper