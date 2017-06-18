# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from employee_manager.models import Department, Employee


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'department',)
    list_filter = ('name', 'email', 'department',)


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
