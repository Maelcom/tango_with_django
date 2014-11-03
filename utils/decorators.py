from functools import wraps
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from urlparse import urlparse
from django.contrib.auth import REDIRECT_FIELD_NAME


# todo: Pop-up login modal window instead of full redirect
def ajax_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return function(request, *args, **kwargs)
        else:
            next_url = urlparse(request.META.get('HTTP_REFERER')).path
            return JsonResponse({'login_required': settings.LOGIN_URL +
                                             '?' + redirect_field_name
                                             + '=' + next_url})
    return _wrapped_view


# Experimental method. If it works, will replace code in @ajax_login_required
def popup_login_required(function=None):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return function(request, *args, **kwargs)
        else:
            return JsonResponse({'login_required': reverse('ajax_login')})
    return _wrapped_view
