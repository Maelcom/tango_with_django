from functools import wraps
from django.http import JsonResponse
from django.core.urlresolvers import reverse


def ajax_login_required(function=None):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return function(request, *args, **kwargs)
        else:
            return JsonResponse({'login_required': reverse('ajax_login')})
    return _wrapped_view
