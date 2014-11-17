from functools import wraps
from django.http import JsonResponse
from django.core.urlresolvers import reverse


def ajax_login_required(function=None):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if request.is_ajax() and not request.user.is_authenticated():
            return JsonResponse({'login_required': reverse('ajax_login')})
        else:
            return function(request, *args, **kwargs)
    return _wrapped_view
