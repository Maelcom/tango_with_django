from django.contrib import admin
from django.db.models import get_models, get_app


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


for model in get_models(get_app('rango')):
    try:
        admin.site.register(model, globals()[model.__name__+'Admin'])
    except admin.sites.AlreadyRegistered:
        pass
    except (NameError, KeyError):
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass
