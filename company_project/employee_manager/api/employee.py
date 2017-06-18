# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from django.views import View

from employee_manager.api_tools import (
    check_auth_token, validate_content_type, clean_request_data
)
from employee_manager.models import Department, Employee


class EmployeeView(View):
    pass
