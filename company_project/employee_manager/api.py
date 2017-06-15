# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse


def health(request):
    response_data = {'content': 'OK'}
    return HttpResponse(
        json.dumps(response_data), content_type="application/json", status=200
    )
