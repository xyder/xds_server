from xds_server.internal_apps.main_interface import views
from xds_server.tools.routing import url

urlpatterns = [
    url('/', view_func=views.index),
]
