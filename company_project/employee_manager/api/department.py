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
from employee_manager.models import Department


class DepartmentView(View):

    @check_auth_token
    @validate_content_type
    def get(self, request, *args, **kwargs):
        departments_list = Department.get_all_as_list_of_dicts()
        response_data = {'content': departments_list}

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
            status=200
        )

    @check_auth_token
    @validate_content_type
    def post(self, request, *args, **kwargs):
        request_data = clean_request_data(request.body)
        department_name = request_data.get('department_name')

        if department_name:
            try:
                department = Department.objects.create(name=department_name)
            except IntegrityError:
                status = 208
                message = 'Department already exists'
                response_data = {'content': message}
            else:
                status = 200
                message = "Department '{}' was added".format(department.name)
                response_data = {'content': message}

        else:
            status = 400
            message = 'Missing data'
            response_data = {'content': message}

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
            status=status
        )

    @check_auth_token
    @validate_content_type
    def put(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        department_id = request_data.get('department_id')
        department_new_name = request_data.get('department_name')

        if department_id and department_new_name:

            try:
                department = Department.objects.get(id=department_id)
            except ObjectDoesNotExist:
                status = 404
                message = "Department not found"

            else:
                old_department_name = department.name
                department.name = department_new_name
                try:
                    department.save()
                except IntegrityError:
                    status = 400
                    message = "Department already exists"
                else:
                    status = 200
                    message = "Department name {} changed to {}".format(
                        old_department_name, department_new_name
                    )

        else:
            status = 400
            message = 'Missing data'
            response_data = {'content': message}

        response_data = {'content': message}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
            status=status
        )

    @check_auth_token
    @validate_content_type
    def delete(self, request, *args, **kwargs):
        request_delete = json.loads(request.body)
        department_name = request_delete.get('department_name')

        if department_name:
            try:
                department = Department.objects.get(name=department_name)
            except ObjectDoesNotExist:
                status = 404
                message = "Department not found"
            else:
                # if it has employees related
                if department.employee_set.count():
                    status = 400
                    message = "Department cannot be deleted: it has employees"
                else:
                    department.delete()
                    status = 200
                    message = "Department '{}' deleted".format(department_name)

        else:
            status = 400
            message = 'Missing data'
            response_data = {'content': message}

        response_data = {'content': message}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
            status=status
        )
