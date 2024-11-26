from communicator.communicator_abc import CommunicatorText


class MockCommunicator(CommunicatorText):
    def write_command(self, command: str):
        print(command, flush=True)
