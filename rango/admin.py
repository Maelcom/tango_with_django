from django.contrib import admin
from django.db.models import get_models, get_app
from django.contrib.sessions.models import Session


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

for model in get_models(get_app('rango')):
    try:
        admin.site.register(model, locals().copy().get(model.__name__+'Admin'))
    except admin.sites.AlreadyRegistered:
        pass
