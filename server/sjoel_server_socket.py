from threading import Thread

import cv2
from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO

from controller.sjoel_controller_base import MovementDirection, SjoelControllerBase
from server.sjoel_server_abc import SjoelServerAbc


def generate_frames(camera_index: int, frame_container: dict):
    cap = cv2.VideoCapture(camera_index)
    try:
        while True:
            ret, frame = cap.read()
            if ret:
                index = frame_container.get(camera_index, {}).get('index', 0)
                frame_container[camera_index] = {'frame': frame, 'index': index + 1}
    finally:
        cap.release()


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
        self.usernames = {}
        self.leader = None

    def init(self):
        self._register_socketio_handlers()
        return self.app

    def video_feed(self, camera_id: str):
        # Start a new thread for the camera if it doesn't exist yet
        # This way we can serve multiple camera feeds at the same time, as well as the same feed to multiple clients
        if camera_id not in self.threads:
            self.threads[camera_id] = Thread(target=generate_frames, args=(int(camera_id), self.frame_container))
            self.threads[camera_id].daemon = True
            self.threads[camera_id].start()

        return Response(serve_frames(int(camera_id), self.frame_container),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    def _is_leader(self, sid):
        return self.leader == sid

    def _register_socketio_handlers(self):
        @self.socketio.on('left')
        def left():
            if not self._is_leader(request.sid):
                return

            pos = self.controller.move(MovementDirection.LEFT)
            self.socketio.emit('position', pos)

        @self.socketio.on('right')
        def right():
            if not self._is_leader(request.sid):
                return

            pos = self.controller.move(MovementDirection.RIGHT)
            self.socketio.emit('position', pos)

        @self.socketio.on('fire')
        def fire():
            if not self._is_leader(request.sid):
                return

            try:
                self.socketio.emit('fire', 'begin fire')
                self.controller.fire()
                self.socketio.emit('fire', 'end fire')
            except RuntimeError as e:
                self.socketio.emit('error', str(e))

        @self.socketio.on('join')
        def join(username):
            print(f"User {username} joined", flush=True)
            self.usernames[request.sid] = username
            self.socketio.emit('users', list(self.usernames.values()))

            # If no leader is set, set the leader to the first user that joins
            if not self.leader:
                self.leader = request.sid
                self.socketio.emit('leader', username)

        @self.socketio.on('leader')
        def leader(username):
            # Only the current leader can change the leader
            if self.leader is not request.sid:
                return

            # Find the new leader
            new_leader = next((sid for sid, name in self.usernames.items() if name == username), None)
            if new_leader is None:
                return

            # Set the new leader
            print(f"User {username} is the new leader", flush=True)
            self.leader = new_leader
            self.socketio.emit('leader', username)

        @self.socketio.on('connect')
        def connect():
            print('client connected', flush=True)

        @self.socketio.on('disconnect')
        def disconnect():
            username = self.usernames.get(request.sid, None)
            if not username:
                return

            # Remove the user
            print(f"User {username} disconnected", flush=True)
            del self.usernames[request.sid]

            # If the leader disconnects, set the leader to the next user
            if request.sid is self.leader:
                self.leader = next(iter(self.usernames), None)
                leader_username = self.usernames.get(self.leader, None)
                self.socketio.emit('leader', leader_username)

            # Update the user list
            self.socketio.emit('users', list(self.usernames.values()))
