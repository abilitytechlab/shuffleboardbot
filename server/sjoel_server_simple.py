from flask import Flask, render_template

from server.sjoel_server_abc import SjoelServerAbc
from settings import HostingSettings
from sjoel_controller import SjoelController


class SjoelServerSimple(SjoelServerAbc):
    def __init__(self, settings: HostingSettings, controller: SjoelController):
        super().__init__(settings, controller)
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
        return str(self.controller.fire())

    def _center(self):
        return str(self.controller.center())

    def run(self):
        self.app.run(host=self.settings.interface, port=self.settings.port, debug=self.settings.debug)
