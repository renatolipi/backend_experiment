# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Employee(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    department = models.ForeignKey(Department)

    def __str__(self):
        return self.name
