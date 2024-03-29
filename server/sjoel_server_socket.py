from flask import Flask, render_template
from flask_socketio import SocketIO

from server.sjoel_server_abc import SjoelServerAbc
from settings import HostingSettings
from sjoel_controller import SjoelController


class SjoelServerSocket(SjoelServerAbc):
    def __init__(self, settings: HostingSettings, controller: SjoelController):
        super().__init__(settings, controller)
        self.app = Flask('Socket sjoel server')
        self.socketio = SocketIO(self.app)

        self.app.route('/')(lambda: render_template('socket.html'))

    def run(self):
        self._register_socketio_handlers()
        self.socketio.run(self.app, host=self.settings.interface, port=self.settings.port, debug=self.settings.debug)

    def _register_socketio_handlers(self):
        @self.socketio.on('left')
        def left():
            pos = self.controller.move('left')
            self.socketio.emit('position', pos)

        @self.socketio.on('right')
        def right():
            pos = self.controller.move('right')
            self.socketio.emit('position', pos)

        @self.socketio.on('fire')
        def fire():
            try:
                self.socketio.emit('fire', 'begin fire')
                self.controller.fire()
                self.socketio.emit('fire', 'end fire')
            except RuntimeError as e:
                self.socketio.emit('error', str(e))

        @self.socketio.on('connect')
        def connect():
            print('client connected')

        @self.socketio.on('disconnect')
        def disconnect():
            print('client disconnected')
