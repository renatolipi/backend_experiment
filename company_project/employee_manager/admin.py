# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


from employee_manager.models import Department, Employee


admin.site.register(Department)
admin.site.register(Employee)
