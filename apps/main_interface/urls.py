from core.routing import url
from . import views

urlpatterns = [
    url('/', view_func=views.index),
]
