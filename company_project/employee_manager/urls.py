from django.conf.urls import url

# from . import views
from employee_manager.api import health, DepartmentView, EmployeeView


urlpatterns = [
    url(r'^api/v1/health$', health, name='health'),
    url(r'^api/v1/department', DepartmentView.as_view(), name='department'),
    url(r'^api/v1/employee', EmployeeView.as_view(), name='employee'),
]
