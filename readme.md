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
