from internal_apps.main_interface import views
from tools.routing import url

urlpatterns = [
    url('/', view_func=views.index),
]
