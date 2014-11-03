from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^category/(?P<category_name_slug>[\w-]+)/add_page/$', views.add_page, name='add_page'),
        url(r'^category/(?P<category_name_slug>[\w-]+)/$', views.category_view, name='category'),
        url(r'^like_category/$', views.like_category, name='like_category'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        url(r'^restricted/$', views.restricted, name='restricted'),
        url(r'^change/$', password_change, {'post_change_redirect': 'index'}, name='change'),
        url(r'^search/$', views.search, name='search'),
        url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
        url(r'^mailer/$', views.mailer, name='mailer'),
        url(r'^goto/$', views.track_url, name='goto'),
        url(r'^profile/$', views.ProfileUpdate.as_view(), name='profile'),
        url(r'^ajax_login/$', views.ajax_login, name='ajax_login'),
)
