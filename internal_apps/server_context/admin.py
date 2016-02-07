from flask.ext.admin.contrib.sqla import ModelView

from xds_server.core import admin
from xds_server.core.database import db_session
from xds_server.internal_apps.server_context import models


# noinspection PyAbstractClass
class ContextParameterModelView(ModelView):
    """
    Custom ModelView for the ContextParameter model.
    """

    column_display_pk = True
    form_columns = ['key', 'value', 'description']

admin.add_view(ContextParameterModelView(models.ContextParameter, db_session))
