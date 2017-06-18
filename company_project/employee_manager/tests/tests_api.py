# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client


class GenericAPITests(TestCase):

    def test_health_with_no_authorization_token(self):
        client = Client()
        headers = {'CONTENT_TYPE': 'application/json'}

        response = client.get('/api/v1/health',
                              data=None,
                              **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"content": "Unauthorized"})

    def test_health_with_no_content_type(self):
        client = Client()
        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF'}

        response = client.get('/api/v1/health',
                              data=None,
                              **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'content': 'Unsupported content_type'})

    def test_health(self):
        client = Client()
        headers = {'HTTP_AUTHORIZATION': '00123456789ABCDEF',
                   'CONTENT_TYPE': 'application/json'}

        response = client.get('/api/v1/health',
                              data=None,
                              **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"content": "OK"})
