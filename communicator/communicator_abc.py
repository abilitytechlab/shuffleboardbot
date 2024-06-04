from abc import ABC, abstractmethod


class CommunicatorText(ABC):
    @abstractmethod
    def write_command(self, command: str):
        """
        Write a command to the serial port
        :param command: The command to write
        """
        pass
