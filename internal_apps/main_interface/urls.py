from core.routing import url
from internal_apps.main_interface import views

urlpatterns = [
    url('/', view_func=views.index),
]
