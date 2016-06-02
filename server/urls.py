from core.routing import url

urlpatterns = [
    url('/bookmarks', include='xds_bookmarks'),
    url('/notes', include='xds_notes'),
    url('/', include='apps.main_interface')
]
