from flask import Flask, render_template

from server.sjoel_server_abc import SjoelServerAbc
from sjoel_controller import SjoelController


class SjoelServerSimple(SjoelServerAbc):
    def __init__(self, controller: SjoelController):
        super().__init__(controller)
        self.app = Flask('Simple sjoel server')
        self.app.route('/')(lambda: render_template('index.html'))
        self.app.route('/left')(self._left)
        self.app.route('/right')(self._right)
        self.app.route('/fire')(self._fire)

    def _left(self):
        return str(self.controller.move('left'))

    def _right(self):
        return str(self.controller.move('right'))

    def _fire(self):
        try:
            return str(self.controller.fire())
        except RuntimeError as e:
            return str(e)

    def _center(self):
        return str(self.controller.center())

    def init(self):
        return self.app
