# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_all_as_list_of_dicts(self):
        departments = self.objects.all()
        list_of_dicts = [item for item in departments.values()]
        return list_of_dicts


@python_2_unicode_compatible
class Employee(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department)

    def __str__(self):
        return self.name

    @classmethod
    def get_all_as_list_of_dicts(self, departments_name_list):
        if departments_name_list:
            employees = self.objects.filter(
                department__name__in=departments_name_list
            )
        else:
            employees = self.objects.all()

        list_of_dicts = []
        for employee in employees:
            item = {'id': employee.id,
                    'name': employee.name,
                    'email': employee.email,
                    'department': employee.department.name}
            list_of_dicts.append(item)
        return list_of_dicts
