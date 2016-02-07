import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# possible keys:
#   module - (mandatory) represents the module used to fetch the routes and build the blueprint
#   prefix - represents the optional prefix that can be used for the routes
#   undefined - represents submodules which will be ignored on dynamic import
INSTALLED_APPS = [
    {
        'module': 'xds_server.internal_apps.main_interface',
        'undefined': ['models', 'admin']
    },
    {
        'module': 'xds_server.internal_apps.server_context',
        'undefined': ['urls']
    },
    {
        'module': 'xds_server_apps.xds_bookmarks',
        'prefix': '/bookmarks'
    }
]

APP_NAME = 'XDS Server'


# config classes
class BaseConfig(object):
    """
    Class containing base application environment configuration
    """

    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (os.path.join(BASE_DIR, 'data.sqlite'))

    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 5000
    SERVER_NAME = ''

    # set the secret key.  keep this really secret:
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    def __init__(self):
        self.build_server_name()

    def build_server_name(self):
        self.SERVER_NAME = '%s:%s' % (self.SERVER_HOST, self.SERVER_PORT)


class ProductionConfig(BaseConfig):
    """
    Class containing the production environment configuration
    """

    SERVER_PORT = 80


class DevelopmentConfig(BaseConfig):
    """
    Class containing the development environment configuration
    """

    DEBUG = True
    SERVER_PORT = 8000


class TestingConfig(BaseConfig):
    """
    Class containing the testing environment configuration
    """

    TESTING = True
    SERVER_PORT = 8000


# change this to run with different configs
ACTIVE_CONFIG = DevelopmentConfig()
