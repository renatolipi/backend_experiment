# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import skip

from django.test import TestCase, Client


class DepartmentApiTests(TestCase):

    @skip("TODO")
    def test_list_departments(self):
        client = Client()
        response = client.get('/api/v1/department')

        # TODO:
        self.assertEqual(response.status_code, 200)
        # TODO:
        self.assertEqual(response.json(), {"content": "OK"})

    @skip("TODO")
    def test_create_department(self):
        client = Client()
        response = client.post('/api/v1/department')

        # TODO:
        self.assertEqual(response.status_code, 200)
        # TODO:
        self.assertEqual(response.json(), {"content": "OK"})

    @skip("TODO")
    def test_create_duplicated_department(self):
        client = Client()
        response = client.post('/api/v1/department')

        # TODO:
        self.assertEqual(response.status_code, 200)
        # TODO:
        self.assertEqual(response.json(), {"content": "OK"})

    # TODO:
    # UPDATE

    # TODO
    # DELETE
