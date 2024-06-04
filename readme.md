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
stepper_axis = "X"              # Axis of the stepper
stepper_step = 10               # How many steps to move the stepper per command
```

## Usage

Before connecting to the raspberry pi, open your windows search bar and search "View network computers and devices", double click your wi-fi and click properties, go to the sharing tab on the top and enable "Allow other network users to connect through this computer's internet connection".

Then connect to the raspberry pi using an ethernet cable. Make sure raspberry pi is on.
Then you can connect to the pi using ssh via the command line or using an extension for your IDE (like vscode).

To connect via the command line write the following:
`ssh boris@raspberrypi.local`

The password is the default raspberrypi password: "raspberry"

Connection with the pi can be spotty and sometimes fail, reconnecting the ethernet cable and/or restarting the pi can help.

To connect using an extension simply requires configuring the connecting, the hostname then is raspberrypi.local and the user is boris.