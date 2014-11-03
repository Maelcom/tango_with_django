from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import UpdateView
from django.http import JsonResponse
from django.shortcuts import render
from registration.backends.simple.views import RegistrationView
from rango.models import UserProfile


def ajax_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return JsonResponse({'login_success': 'ok'})
    return render(request, 'rango/ajax_login.html', {'form': form})


class RangoRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/rango/'


class ProfileUpdate(UpdateView):
    model = UserProfile
    fields = ('picture', 'website')
    template_name_suffix = ""
    template_name = 'rango/profile.html'
    success_url = '.'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
