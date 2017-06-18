# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import skip

from django.test import TestCase, Client

from employee_manager.models import Department, Employee


class EmployeeListingTests(TestCase):

    @skip("TODO")
    def test_list_employees(self):
        client = Client()
        response = client.get('/api/v1/department')

        # TODO:
        self.assertEqual(response.status_code, 200)
        # TODO:
        self.assertEqual(response.json(), {"content": "OK"})

    @skip("TODO")
    def test_list_employees_from_a_specific_department(self):
        client = Client()
        response = client.get('/api/v1/department?name=Mobile')

        # TODO:
        self.assertEqual(response.status_code, 200)
        # TODO:
        self.assertEqual(response.json(), {"content": "OK"})


class EmployeeCreatingTests(TestCase):
    @skip("TODO")
    def test_list_departments(self):
        pass

    # no content_type

    # no authorization

    # creating duplicated employee

    # missing or wrong data

    # creating sucess


class EmployeeUpdatingTests(TestCase):
    @skip("TODO")
    def test_list_departments(self):
        pass

    # no content_type

    # no authorization

    # updating non existent

    # updating to an already existent

    # updating successfull


class EmployeeDeletingTests(TestCase):
    @skip("TODO")
    def test_list_departments(self):
        pass

    # no content_type

    # no authorization

    # deleting non existent

    # deleting successfull

