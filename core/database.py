from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from xds_server.core.lib import import_models

from xds_server.server.settings import ACTIVE_CONFIG

# the database engine
engine = create_engine(ACTIVE_CONFIG.SQLALCHEMY_DATABASE_URI)

# the database session
db_session = scoped_session(sessionmaker(bind=engine))

# Base model for all models
Base = declarative_base()
Base.query = db_session.query_property()


def init_db() -> None:
    """
    Initializes the database and builds tables for models if needed.
    """

    import_models()
    Base.metadata.create_all(bind=engine)
