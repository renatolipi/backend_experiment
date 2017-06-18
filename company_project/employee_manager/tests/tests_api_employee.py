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
        self.headers = {'CONTENT_TYPE': 'application/json',
                        'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

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

    def test_update_missing_parameters(self):
        department1 = Department.objects.create(name="Tech")
        department2 = Department.objects.create(name="Mobile")
        Employee.objects.create(name='Droid Bot',
                                email='one@testc.om',
                                department=department1)
        Employee.objects.create(name='Foolano',
                                email='two@testc.om',
                                department=department2)

        data = {"id": "2",
                "employee_name": "Jack",
                "employee_email": "three@testc.om"}

        response = self.client.put('/api/v1/employee',
                                   json.dumps(data),
                                   content_type='application/json',
                                   **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': "Missing data"})

        self.assertEqual(Employee.objects.count(), 2)

    def test_update_nonexistent_employee(self):
        department = Department.objects.create(name="Tech")
        Employee.objects.create(name='Droid Bot',
                                email='one@testc.om',
                                department=department)

        data = {"employee_id": "3",
                "employee_name": "Jack",
                "employee_email": "three@testc.om",
                "employee_department": "Tech"}

        response = self.client.put('/api/v1/employee',
                                   json.dumps(data),
                                   content_type='application/json',
                                   **self.headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
                         {'content': "Employee not found"})
        self.assertEqual(Employee.objects.count(), 1)

    def test_update_to_nonexistent_department(self):
        department = Department.objects.create(name="Tech")
        Department.objects.create(name="Mobile")
        Employee.objects.create(name='Droid Bot',
                                email='one@testc.om',
                                department=department)

        data = {"employee_id": "1",
                "employee_name": "Jack",
                "employee_email": "three@testc.om",
                "employee_department": "Financial"}

        response = self.client.put('/api/v1/employee',
                                   json.dumps(data),
                                   content_type='application/json',
                                   **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': "Department not found"})

        self.assertEqual(Employee.objects.count(), 1)
        employee = Employee.objects.get(email='one@testc.om')
        self.assertTrue(employee.department.name, department.name)
        self.assertFalse(employee.department.name == 'Financial')

    def test_update_employee_to_existing_email(self):
        department1 = Department.objects.create(name="Tech")
        department2 = Department.objects.create(name="Mobile")
        Employee.objects.create(name='Droid Bot',
                                email='one@testc.om',
                                department=department1)
        Employee.objects.create(name='Foolano',
                                email='two@testc.om',
                                department=department2)

        data = {"employee_id": "1",
                "employee_name": "Droid",
                "employee_email": "two@testc.om",
                "employee_department": "Mobile"}

        response = self.client.put('/api/v1/employee',
                                   json.dumps(data),
                                   content_type='application/json',
                                   **self.headers)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(),
                         {'content': "Another user already has this email"})

    def test_update_succesfully(self):
        department1 = Department.objects.create(name="Tech")
        department2 = Department.objects.create(name="Mobile")
        Employee.objects.create(name='Droid Bot',
                                email='one@testc.om',
                                department=department1)
        Employee.objects.create(name='Foolano',
                                email='two@testc.om',
                                department=department2)

        data = {"employee_id": "2",
                "employee_name": "Jack",
                "employee_email": "three@testc.om",
                "employee_department": "Tech"}

        response = self.client.put('/api/v1/employee',
                                   json.dumps(data),
                                   content_type='application/json',
                                   **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'content': "Employee updated"})

        self.assertEqual(Employee.objects.count(), 2)
        self.assertFalse(Employee.objects.filter(email='two@testc.om'))
        self.assertTrue(Employee.objects.filter(email='three@testc.om'))


class EmployeeDeletingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.headers = {'CONTENT_TYPE': 'application/json',
                        'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

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

    def test_delete_missing_or_wrong_parameters(self):
        department = Department.objects.create(name="Financial")
        Employee.objects.create(name='Droid Bot',
                                email="one@testc.om",
                                department=department)

        data = {"email": "another@testc.om"}

        response = self.client.delete('/api/v1/employee',
                                      json.dumps(data),
                                      content_type='application/json',
                                      **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': "Missing data"})

    def test_delete_nonexistent_employee(self):
        data = {"employee_email": "another@testc.om"}

        response = self.client.delete('/api/v1/employee',
                                      json.dumps(data),
                                      content_type='application/json',
                                      **self.headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
                         {'content': "Employee not found"})

    def test_delete_successfully(self):
        department = Department.objects.create(name="Financial")
        Employee.objects.create(name='Droid Bot',
                                email="one@testc.om",
                                department=department)

        data = {"employee_email": "one@testc.om"}

        response = self.client.delete('/api/v1/employee',
                                      json.dumps(data),
                                      content_type='application/json',
                                      **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'content': "Employee 'one@testc.om' deleted"})
