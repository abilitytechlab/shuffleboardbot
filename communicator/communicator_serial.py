import serial

from communicator.communicator_abc import CommunicatorText


class SerialCommunicator(CommunicatorText):
    def __init__(self, port: str, baud: int):
        """
        A class that communicates with the robot over serial
        :param port: The port to connect to, e.g. COM3
        :param baud: The baud rate to use
        """
        self.port = port
        self.baud = baud

        self.ser = serial.Serial(self.port, self.baud)

        if not self.ser.is_open:
            self.ser.open()

    def __del__(self):
        """
        Close the serial connection when the object is destroyed
        """
        try:
            self.ser.close()
        except AttributeError:
            pass

    def write_command(self, command: str):
        """
        Write a command to the serial port
        :param command: The command to write
        """
        self.ser.write(str.encode(command + "\r\n"))
