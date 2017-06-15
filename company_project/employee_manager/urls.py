from django.conf.urls import url

# from . import views
from . import api

urlpatterns = [
    url(r'^api/v1/health$', api.health, name='health'),
]
