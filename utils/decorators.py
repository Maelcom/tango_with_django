from functools import wraps
from django.conf import settings
from django.http import JsonResponse
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
            return JsonResponse({'redirect': settings.LOGIN_URL +
                                             '?' + redirect_field_name
                                             + '=' + next_url})
    return _wrapped_view
