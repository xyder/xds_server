from sqlalchemy import Column, Text
from xds_server.core.database import Base
from xds_server.core.lib import get_custom_prefixer
from xds_server.internal_apps.server_context import APP_NAME

prefixer = get_custom_prefixer(APP_NAME)


class ContextParameter(Base):
    """
    Model for a context parameter which serves as a store for (key, value) pairs and can be used for
    as an application context.
    """

    __tablename__ = prefixer('context_parameters')

    key = Column(Text, primary_key=True)
    value = Column(Text)
    description = Column(Text)

    def __repr__(self):
        return self.key
