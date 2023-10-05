import time

import serial
from flask import Flask, render_template

app = Flask(__name__)

pos = 0
ser = serial.Serial('COM3', 250000)

@app.route('/fire')
def fire():
    global ser
    ser.write(str.encode("M280 P0 S180\r\n"))
    time.sleep(1)
    ser.write(str.encode("M280 P0 S120\r\n"))
    return 'shoot'

@app.route('/left')
def left():
    global pos
    global ser
    pos -= 10
    ser.write(str.encode(f"G0 X{pos}\r\n"))
    return str(pos)


@app.route('/right')
def right():
    global pos
    global ser
    pos += 10
    ser.write(str.encode(f"G0 X{pos}\r\n"))
    return str(pos)


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    ser.write(str.encode("M280 P0 S120\r\n"))
    app.run(host="192.168.43.148", port=5000, debug=True)
