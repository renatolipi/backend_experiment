# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import wraps
import json

from django.http import HttpResponse

from company_project.settings import (API_ACCEPTABLE_CONTENT_TYPES,
                                      AUTHORIZATION_TOKENS)


def _validate_auth(token):
    return token in AUTHORIZATION_TOKENS


def _get_META(request):
    try:
        meta = request.META
    except AttributeError:
        meta = request.request.META
    finally:
        return meta


def check_auth_token(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        meta = _get_META(request)
        auth_code = meta.get('HTTP_AUTHORIZATION')
        if auth_code:
            if _validate_auth(auth_code):
                return view(request, *args, **kwargs)

        response_data = {'content': 'Unauthorized'}
        return HttpResponse(
            {json.dumps(response_data)},
            content_type="application/json",
            status=401
        )
    return wrapped


def validate_content_type(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        meta = _get_META(request)
        content_type = meta.get('CONTENT_TYPE')
        if not content_type or content_type.lower() not in API_ACCEPTABLE_CONTENT_TYPES:
            response_data = {'content': 'Unsupported content_type'}
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json",
                status=400
            )
        else:
            return view(request, *args, **kwargs)

    return wrapped


def clean_request_data(request_data):
    try:
        result = json.loads(request_data)
    except ValueError:
        result = {}

    return result
