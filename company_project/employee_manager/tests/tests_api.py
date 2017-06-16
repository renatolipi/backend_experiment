# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client


class GenericAPITests(TestCase):

    def test_health(self):
        client = Client()
        response = client.get('/api/v1/health')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"content": "OK"})
