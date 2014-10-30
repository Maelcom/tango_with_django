from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^category/(?P<category_name_slug>[\w-]+)/add_page/$', views.add_page, name='add_page'),
        url(r'^category/(?P<category_name_slug>[\w-]+)/$', views.category_view, name='category'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        # Decomission of handmade login and register
        # Switched to django-registration-redux
        # url(r'^register/$', views.register, name='register'),
        # url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^restricted/$', views.restricted, name='restricted'),
        url(r'^change/$', password_change, {'post_change_redirect': 'index'}, name='change'),
        url(r'^search/$', views.search, name='search'),
        url(r'^mailer/$', views.mailer, name='mailer'),
)
