# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.test import TestCase, Client

from employee_manager.models import Department, Employee


class EmployeeListingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.headers = {'CONTENT_TYPE': 'application/json',
                        'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

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
        response = self.client.get('/api/v1/employees',
                                   data=None,
                                   **self.headers)

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

        response = self.client.get('/api/v1/employees',
                                   data=None,
                                   **self.headers)

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

        response = self.client.get('/api/v1/employees',
                                   data=None,
                                   **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()['content'], list)
        self.assertEqual(len(response.json()['content']), 2)

        response = self.client.get('/api/v1/employees?department=Financial',
                                   data=None,
                                   **self.headers)

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

        response = self.client.get('/api/v1/employees?department=HR,Mobile',
                                   data=None,
                                   **self.headers)

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

        response = self.client.get('/api/v1/employees?department=Mobile,Final',
                                   data=None,
                                   **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()['content'], list)
        self.assertEqual(len(response.json()['content']), 1)


class EmployeeCreatingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.headers = {'CONTENT_TYPE': 'application/json',
                        'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

    def test_create_employee_with_no_authorization_token(self):
        headers = {'CONTENT_TYPE': 'application/json'}

        data = {}

        response = self.client.post('/api/v1/employee',
                                    data=data,
                                    **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"content": "Unauthorized"})

    def test_create_employee_with_no_content_type(self):
        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

        data = {}

        response = self.client.post('/api/v1/employee',
                                    data=data,
                                    **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Unsupported content_type'})

    def test_create_employee_missing_or_wrong_data(self):
        data = None

        response = self.client.post('/api/v1/employee',
                                    data=data,
                                    content_type='application/json',
                                    **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Missing data'})
        self.assertEqual(Department.objects.count(), 0)

        data = {'name': 'Foolano', 'email': 'one@testc.om', 'department': 'HR'}

        response = self.client.post('/api/v1/employee',
                                    data=data,
                                    content_type='application/json',
                                    **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Missing data'})
        self.assertEqual(Department.objects.count(), 0)

    def test_create_user_successfully(self):
        Department.objects.create(name='Mobile')
        data = {"employee_name": "Foolano",
                "employee_email": "one@testc.om",
                "employee_department": "Mobile"}

        response = self.client.post('/api/v1/employee',
                                    json.dumps(data),
                                    content_type='application/json',
                                    **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'content': "Employee 'Foolano' was added"})
        self.assertEqual(Department.objects.count(), 1)

    def test_create_user_with_same_email(self):
        department = Department.objects.create(name='Mobile')
        Department.objects.create(name='Financial')
        Employee.objects.create(name='Droid Bot',
                                email="one@testc.om",
                                department=department)

        data = {"employee_name": "Foolano",
                "employee_email": "one@testc.om",
                "employee_department": "Financial"}

        response = self.client.post('/api/v1/employee',
                                    json.dumps(data),
                                    content_type='application/json',
                                    **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': "Employee already exists"})


class EmployeeUpdatingTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_update_employee_with_no_authorization_token(self):
        headers = {'CONTENT_TYPE': 'application/json'}

        data = {}

        response = self.client.put('/api/v1/employee',
                                   data=data,
                                   **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"content": "Unauthorized"})

    def test_update_employee_with_no_content_type(self):
        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

        data = {}

        response = self.client.put('/api/v1/employee',
                                   data=data,
                                   **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Unsupported content_type'})

    # updating non existent

    # updating to an already existent

    # updating successfull


class EmployeeDeletingTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_delete_employee_with_no_authorization_token(self):
        headers = {'CONTENT_TYPE': 'application/json'}

        data = {}

        response = self.client.delete('/api/v1/employee',
                                      data=data,
                                      **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"content": "Unauthorized"})

    def test_delete_employee_with_no_content_type(self):
        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

        data = {}

        response = self.client.delete('/api/v1/employee',
                                      data=data,
                                      **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Unsupported content_type'})

    # deleting non existent

    # deleting successfull

