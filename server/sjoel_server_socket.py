import cv2
from flask import Flask, render_template, Response
from flask_socketio import SocketIO

from controller.sjoel_controller_base import MovementDirection
from server.sjoel_server_abc import SjoelServerAbc
from controller.sjoel_controller_gcode import SjoelControllerGcode


def generate_frames(camera_index: int):
    cap = cv2.VideoCapture(camera_index)
    while True:
        ret, frame = cap.read()
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')
        else:
            break


class SjoelServerSocket(SjoelServerAbc):
    def __init__(self, controller: SjoelControllerGcode):
        super().__init__(controller)
        self.app = Flask('Socket sjoel server', )
        self.socketio = SocketIO(self.app)
        self.app.route('/')(lambda: render_template('socket.html'))
        self.app.route('/video_feed/<camera_id>')(self.video_feed)

    def init(self):
        self._register_socketio_handlers()
        return self.app

    @staticmethod
    def video_feed(camera_id: str):
        return Response(generate_frames(int(camera_id)), mimetype='multipart/x-mixed-replace; boundary=frame')

    def _register_socketio_handlers(self):
        @self.socketio.on('left')
        def left():
            pos = self.controller.move(MovementDirection.LEFT)
            self.socketio.emit('position', pos)

        @self.socketio.on('right')
        def right():
            pos = self.controller.move(MovementDirection.RIGHT)
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
