import logging

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.socketio import SocketIO

from core.database import init_db
from core.lib import import_admin_views
from core.routing import register_blueprints
from server import settings

# initialize and configure the flask server
app = Flask(__name__, static_folder=settings.STATIC_DIR, static_url_path='/static')
app.config.from_object(settings.ACTIVE_CONFIG)

logger = logging.getLogger('xds_server')

log_handler = logging.StreamHandler()
log_formatter = logging.Formatter(fmt='%(asctime)s -- %(levelname)-9s: %(message)s ----- @[%(pathname)s:%(lineno)d]')
log_formatter.default_time_format = '%y%m%d:%H%M%S'
log_formatter.default_msec_format = '%s:%3d'
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.DEBUG)

logger.addHandler(log_handler)
in_development = app.debug or app.testing
logger.setLevel(logging.DEBUG if in_development else logging.INFO)

socketio = SocketIO(app)

# initialize the admin manager
admin = Admin(app, name=settings.APP_NAME, template_mode='bootstrap3')


def initialize():
    """
    Initializes the application.
    """

    register_blueprints(app, settings.INSTALLED_APPS)
    init_db()
    import_admin_views()
