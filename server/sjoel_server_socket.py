from threading import Thread

import cv2
from flask import Flask, render_template, Response
from flask_socketio import SocketIO

from controller.sjoel_controller_base import MovementDirection, SjoelControllerBase
from server.sjoel_server_abc import SjoelServerAbc


def generate_frames(camera_index: int, frame_container: dict):
    cap = cv2.VideoCapture(camera_index)
    while True:
        ret, frame = cap.read()
        if ret:
            index = frame_container.get(camera_index, {}).get('index', 0)
            frame_container[camera_index] = {'frame': frame, 'index': index + 1}


def serve_frames(camera_index: int, frame_container: dict):
    while True:
        frame = frame_container.get(camera_index, None)
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'
                   + cv2.imencode('.jpg', frame['frame'])[1].tobytes()
                   + b'\r\n')


class SjoelServerSocket(SjoelServerAbc):
    def __init__(self, controller: SjoelControllerBase):
        super().__init__(controller)
        self.app = Flask('Socket sjoel server', )
        self.socketio = SocketIO(self.app)
        self.app.route('/')(lambda: render_template('socket.html'))
        self.app.route('/video_feed/<camera_id>')(self.video_feed)

        self.frame_container = {}
        self.threads = {}

    def init(self):
        self._register_socketio_handlers()
        return self.app

    def video_feed(self, camera_id: str):
        if camera_id not in self.threads:
            self.threads[camera_id] = Thread(target=generate_frames, args=(int(camera_id), self.frame_container))
            self.threads[camera_id].daemon = True
            self.threads[camera_id].start()

        return Response(serve_frames(int(camera_id), self.frame_container),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

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
