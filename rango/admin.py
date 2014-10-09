from django.contrib import admin
from django.db.models import get_models, get_app


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

for model in get_models(get_app('rango')):
    try:
        admin.site.register(model, locals().copy().get(model.__name__+'Admin'))
    except admin.sites.AlreadyRegistered:
        pass
