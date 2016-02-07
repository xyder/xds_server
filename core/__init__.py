import logging
from flask import Flask
from flask.ext.admin import Admin

from xds_server.core.database import init_db
from xds_server.core.lib import import_admin_views
from xds_server.server import settings
from xds_server.tools.routing import register_blueprints


# initialize and configure the flask server
app = Flask(__name__)
app.config.from_object(settings.ACTIVE_CONFIG)

# set logger level for production
if not app.debug and not app.testing:
    logging.getLogger('wekzeug').setLevel(logging.WARNING)

# initialize the admin manager
admin = Admin(app, name=settings.APP_NAME, template_mode='bootstrap3')


def initialize():
    """
    Initializes the application.
    """

    register_blueprints(app, settings.INSTALLED_APPS)
    init_db()
    import_admin_views()
