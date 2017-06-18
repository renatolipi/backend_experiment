# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from django.http import HttpResponse

from employee_manager.api_tools import check_auth_token, validate_content_type


logger = logging.getLogger(__name__)


@check_auth_token
@validate_content_type
def health(request):
    logger.debug('health checking')
    response_data = {'content': 'OK'}
    return HttpResponse(
        json.dumps(response_data), content_type="application/json", status=200
    )
