from flask import Flask, render_template
from settings import HostingSettings
from sjoel_controller import SjoelController


class SjoelServerSimple:
    def __init__(self, settings: HostingSettings, controller: SjoelController):
        self.controller = controller

        self.app = Flask('Simple sjoel server')
        self.app.route('/')(self._index)
        self.app.route('/left')(self._left)
        self.app.route('/right')(self._right)
        self.app.route('/fire')(self._fire)

        self.settings = settings

    def _index(self):
        return render_template('index.html')

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
