# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url, include
from .views import HomePageView, ScheduleView, SessionView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^schedule$', ScheduleView.as_view(), name='schedule'),
    url(r'^session$', SessionView.as_view(), name='session'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('demo.views',
    url(r'^session/add/$', 'add_session', name='add_session'),
    url(r'^session/edit/(?P<id>.+)/$', 'edit_session', name='edit_session'),
)
