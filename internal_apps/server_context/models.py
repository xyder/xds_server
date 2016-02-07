from sqlalchemy import Column, Text
from xds_server.core.database import Base


class ContextParameter(Base):
    """
    Model for a context parameter which serves as a store for (key, value) pairs and can be used for
    as an application context.
    """

    __tablename__ = 'context_parameters'

    key = Column(Text, primary_key=True)
    value = Column(Text)
    description = Column(Text)

    def __repr__(self):
        return self.key
