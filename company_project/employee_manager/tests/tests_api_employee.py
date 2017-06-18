# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import skip

from django.test import TestCase, Client

from employee_manager.models import Department, Employee


class EmployeeListingTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_list_employee_with_no_authorization_token(self):
        headers = {'CONTENT_TYPE': 'application/json'}

        response = self.client.get('/api/v1/employee',
                                   data=None,
                                   **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"content": "Unauthorized"})

    def test_list_employee_with_no_content_type(self):
        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

        response = self.client.get('/api/v1/employee',
                                   data=None,
                                   **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Unsupported content_type'})

    def test_list_employees_has_no_entries(self):
        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF',
                   'CONTENT_TYPE': 'application/json'}

        response = self.client.get('/api/v1/employees',
                                   data=None,
                                   **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"content": []})

    def test_list_employees_has_entries(self):
        department = Department.objects.create(name='HR')
        Employee.objects.create(name="Foolano",
                                email='one@testc.om',
                                department=department)
        Employee.objects.create(name="Droid Bot",
                                email='two@testc.om',
                                department=department)

        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF',
                   'CONTENT_TYPE': 'application/json'}

        response = self.client.get('/api/v1/employees',
                                   data=None,
                                   **headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()['content'], list)
        self.assertEqual(len(response.json()['content']), 2)

    def test_list_employees_from_a_specific_department(self):
        department1 = Department.objects.create(name='HR')
        department2 = Department.objects.create(name='Financial')
        Employee.objects.create(name="Foolano",
                                email='one@testc.om',
                                department=department1)
        Employee.objects.create(name="Droid Bot",
                                email='two@testc.om',
                                department=department2)

        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF',
                   'CONTENT_TYPE': 'application/json'}

        response = self.client.get('/api/v1/employees',
                                   data=None,
                                   **headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()['content'], list)
        self.assertEqual(len(response.json()['content']), 2)

        response = self.client.get('/api/v1/employees?department=Financial',
                                   data=None,
                                   **headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()['content'], list)
        self.assertEqual(len(response.json()['content']), 1)

    def test_list_employees_from_multiple_departments_filter(self):
        department1 = Department.objects.create(name='HR')
        department2 = Department.objects.create(name='Financial')
        department3 = Department.objects.create(name='Mobile')
        Employee.objects.create(name="Foolano",
                                email='one@testc.om',
                                department=department1)
        Employee.objects.create(name="Droid Bot",
                                email='two@testc.om',
                                department=department2)
        Employee.objects.create(name="Space Ghost",
                                email='three@testc.om',
                                department=department3)

        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF',
                   'CONTENT_TYPE': 'application/json'}

        response = self.client.get('/api/v1/employees?department=HR,Mobile',
                                   data=None,
                                   **headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()['content'], list)
        self.assertEqual(len(response.json()['content']), 2)

    def test_list_employees_from_multiple_departments_filter_one_wrong(self):
        department1 = Department.objects.create(name='HR')
        department2 = Department.objects.create(name='Financial')
        department3 = Department.objects.create(name='Mobile')
        Employee.objects.create(name="Foolano",
                                email='one@testc.om',
                                department=department1)
        Employee.objects.create(name="Droid Bot",
                                email='two@testc.om',
                                department=department2)
        Employee.objects.create(name="Space Ghost",
                                email='three@testc.om',
                                department=department3)

        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF',
                   'CONTENT_TYPE': 'application/json'}

        response = self.client.get('/api/v1/employees?department=Mobile,Final',
                                   data=None,
                                   **headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()['content'], list)
        self.assertEqual(len(response.json()['content']), 1)


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

