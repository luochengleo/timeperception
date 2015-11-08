from django.conf.urls import patterns, include, url
from django.contrib import admin
from readanno.views import login
from readanno.views import jobs
from readanno.views import calibrate
from readanno.views import read
from readanno.views import feedback
from readanno.views import docservice
from readanno.views import log
# login _ no parameter;
# tasks/#setting
# calibrate/#setting/#task
# read/#settings
# feedback/#setting




urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/$', login),
                       url(r'^jobs/(\d{1,2})/$', jobs),
                       url(r'^calibrate/(\d{1,2})/(\d{1,2})/$', calibrate),
                       url(r'^read/(\d{1,2})/(\d{1,2})/$', read),
                       url(r'^feedback/(\d{1,2})/$', feedback),
                       url(r'^docservice/(\d{1,2})/(\d{1,2})/$',docservice),
                       url(r'^LogService/$', log)
                       )

