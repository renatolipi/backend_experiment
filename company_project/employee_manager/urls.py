from django.conf.urls import url

# from . import views
from employee_manager.api import health, DepartmentView


urlpatterns = [
    url(r'^api/v1/health$', health, name='health'),
    url(r'^api/v1/department', DepartmentView.as_view(), name='department'),
]
