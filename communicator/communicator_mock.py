from communicator.communicator_abc import CommunicatorAbc


class MockCommunicator(CommunicatorAbc):
    def write_command(self, command: str):
        print(command)
