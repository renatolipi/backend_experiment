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

    @check_auth_token
    @validate_content_type
    def get(self, request, *args, **kwargs):
        from_departments = request.GET.get('department', None)
        if from_departments:
            from_departments = from_departments.split(',')

        employees_list = Employee.get_all_as_list_of_dicts(from_departments)
        response_data = {'content': employees_list}

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
            status=200
        )

    @check_auth_token
    @validate_content_type
    def post(self, request, *args, **kwargs):
        pass

    @check_auth_token
    @validate_content_type
    def put(self, request, *args, **kwargs):
        pass

    @check_auth_token
    @validate_content_type
    def delete(self, request, *args, **kwargs):
        pass
