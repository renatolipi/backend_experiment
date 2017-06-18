# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.test import TestCase, Client

from employee_manager.models import Department, Employee


class DepartmentListingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF',
                        'CONTENT_TYPE': 'application/json'}

    def test_list_department_with_no_authorization_token(self):
        headers = {'CONTENT_TYPE': 'application/json'}

        response = self.client.get('/api/v1/department',
                                   data=None,
                                   **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"content": "Unauthorized"})

    def test_list_department_with_no_content_type(self):
        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

        response = self.client.get('/api/v1/department',
                                   data=None,
                                   **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Unsupported content_type'})

    def test_list_departments_has_no_entries(self):

        response = self.client.get('/api/v1/department',
                                   data=None,
                                   **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"content": []})

    def test_list_departments_has_entries(self):
        Department.objects.create(name="Human Resources")
        Department.objects.create(name="Financial")

        response = self.client.get('/api/v1/department',
                                   data=None,
                                   **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"content": [{u'id': 1, u'name': u'Human Resources'},
                         {u'id': 2, u'name': u'Financial'}]}
        )


class DepartmentCreatingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF',
                        'CONTENT_TYPE': 'application/json'}

    def test_create_department_with_no_authorization_token(self):
        headers = {'CONTENT_TYPE': 'application/json'}

        data = {"department_name": "Technology"}

        response = self.client.post('/api/v1/department',
                                    data=data,
                                    **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"content": "Unauthorized"})
        self.assertEqual(Department.objects.count(), 0)

    def test_create_department_with_no_content_type(self):
        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

        data = {'department_name': 'Technology'}

        response = self.client.post('/api/v1/department',
                                    data=data,
                                    **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Unsupported content_type'})
        self.assertEqual(Department.objects.count(), 0)

    def test_create_department_missing_or_wrong_data(self):
        data = None

        response = self.client.post('/api/v1/department',
                                    data=data,
                                    **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Missing data'})
        self.assertEqual(Department.objects.count(), 0)

        data = {'name': 'Technology'}

        response = self.client.post('/api/v1/department',
                                    data=data,
                                    **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Missing data'})
        self.assertEqual(Department.objects.count(), 0)

    def test_create_department_successfully(self):
        data = {"department_name": "Techonology"}

        response = self.client.post('/api/v1/department',
                                    json.dumps(data),
                                    content_type='application/json',
                                    **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'content': "Department 'Techonology' was added"})
        self.assertEqual(Department.objects.count(), 1)

    def test_create_department_with_existent_name(self):
        Department.objects.create(name="Financial")

        data = {"department_name": "Financial"}

        response = self.client.post('/api/v1/department',
                                    json.dumps(data),
                                    content_type='application/json',
                                    **self.headers)

        self.assertEqual(response.status_code, 208)
        self.assertEqual(response.json(),
                         {'content': 'Department already exists'})


class DepartmentUpdatingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF',
                        'CONTENT_TYPE': 'application/json'}

    def test_update_department_with_no_authorization_token(self):
        headers = {'CONTENT_TYPE': 'application/json'}

        data = {"department_name": "Technology"}

        response = self.client.put('/api/v1/department',
                                   data=data,
                                   **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"content": "Unauthorized"})

    def test_update_department_with_no_content_type(self):
        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

        data = {'department_name': 'Technology'}

        response = self.client.put('/api/v1/department',
                                   data=data,
                                   **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Unsupported content_type'})

    def test_update_missing_or_wrong_data(self):
        Department.objects.create(name="Tech")
        Department.objects.create(name="Mobile")
        data = {'id': '1', 'name': 'Technology'}

        response = self.client.put('/api/v1/department',
                                   json.dumps(data),
                                   content_type='application/json',
                                   **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Missing data'})

    def test_update_nonexistent_department(self):
        data = {"department_id": "1",
                "department_name": "Techonology"}

        response = self.client.put('/api/v1/department',
                                   json.dumps(data),
                                   content_type='application/json',
                                   **self.headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
                         {'content': "Department not found"})

    def test_update_existing_department_name(self):
        Department.objects.create(name="Financial")
        Department.objects.create(name="Technology")

        data = {"department_id": "1",
                "department_name": "Technology"}

        response = self.client.put('/api/v1/department',
                                   json.dumps(data),
                                   content_type='application/json',
                                   **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': "Department already exists"})

    def test_update_successfully(self):
        Department.objects.create(name="Financial")
        Department.objects.create(name="Tech")

        data = {"department_id": "2",
                "department_name": "Mobile"}

        response = self.client.put('/api/v1/department',
                                   json.dumps(data),
                                   content_type='application/json',
                                   **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'content': "Department name Tech changed to Mobile"})

        self.assertEqual(Department.objects.count(), 2)
        department_names = Department.objects.values('name').all()
        department_names = [item.get('name') for item in department_names]
        self.assertTrue('Financial' in department_names)
        self.assertTrue('Mobile' in department_names)
        self.assertFalse('Tech' in department_names)


class DepartmentDeletingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF',
                        'CONTENT_TYPE': 'application/json'}

    def test_delete_department_with_no_authorization_token(self):
        headers = {'CONTENT_TYPE': 'application/json'}

        data = {"department_name": "Technology"}

        response = self.client.delete('/api/v1/department',
                                      data=data,
                                      **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"content": "Unauthorized"})

    def test_delete_department_with_no_content_type(self):
        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

        data = {'department_name': 'Technology'}

        response = self.client.delete('/api/v1/department',
                                      data=data,
                                      **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Unsupported content_type'})

    def test_delete_with_missing_or_wrong_parameters(self):
        Department.objects.create(name="Financial")

        data = {"name": "Financial"}

        response = self.client.delete('/api/v1/department',
                                      json.dumps(data),
                                      content_type='application/json',
                                      **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': "Missing data"})

    def test_delete_nonexistent_department(self):
        data = {"department_name": "Techonology"}

        response = self.client.delete('/api/v1/department',
                                      json.dumps(data),
                                      content_type='application/json',
                                      **self.headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
                         {'content': "Department not found"})

    def test_delete_successfully(self):
        Department.objects.create(name="Financial")

        data = {"department_name": "Financial"}

        response = self.client.delete('/api/v1/department',
                                      json.dumps(data),
                                      content_type='application/json',
                                      **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'content': "Department 'Financial' deleted"})

    def test_cannot_delete_when_employees_are_attached(self):
        dept = Department.objects.create(name="Financial")
        Employee.objects.create(name="Foolano",
                                email="eee@mail.inf",
                                department=dept)

        data = {"department_name": "Financial"}

        response = self.client.delete('/api/v1/department',
                                      json.dumps(data),
                                      content_type='application/json',
                                      **self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {'content': "Department cannot be deleted: it has employees"}
        )
