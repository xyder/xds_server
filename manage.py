# noinspection PyUnresolvedReferences
# relative import of settings where the working directory is added to PYTHONPATH
import server.settings

from xds_server.core import initialize, app
from xds_server.core.database import db_session


# noinspection PyUnusedLocal
@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Executes on each session end.
    """

    db_session.remove()

if __name__ == '__main__':
    initialize()

    app.run()
