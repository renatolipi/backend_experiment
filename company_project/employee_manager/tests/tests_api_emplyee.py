# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import skip

from django.test import TestCase, Client


class EmployeeApiTests(TestCase):

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

    @skip("TODO")
    def test_create_employee_successfully(self):
        client = Client()
        response = client.post('/api/v1/department')

        # TODO:
        self.assertEqual(response.status_code, 200)
        # TODO:
        self.assertEqual(response.json(), {"content": "OK"})

    @skip("TODO")
    def test_create_duplicated_employee(self):
        client = Client()
        response = client.post('/api/v1/department/id/employee')

        # TODO:
        self.assertEqual(response.status_code, 200)
        # TODO:
        self.assertEqual(response.json(), {"content": "OK"})

    @skip("TODO")
    def test_create_employee_with_nonexistent_department(self):
        client = Client()
        response = client.post('/api/v1/department/id/employee')

        # TODO:
        self.assertEqual(response.status_code, 200)
        # TODO:
        self.assertEqual(response.json(), {"content": "OK"})

    # TODO:

    # UPDATE
    # DELETE
