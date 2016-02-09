from flask.ext.admin.contrib.sqla import ModelView

from xds_server.core.lib import create_admin_view
from xds_server.internal_apps.server_context import models


# noinspection PyAbstractClass
class ContextParameterModelView(ModelView):
    """
    Custom ModelView for the ContextParameter model.
    """

    column_display_pk = True
    form_columns = ['key', 'value', 'description']


create_admin_view(models.ContextParameter, model_view=ContextParameterModelView)
