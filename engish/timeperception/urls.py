from django.conf.urls import patterns, include, url
from django.contrib import admin
from readanno.views import login, docquestionservice, docoptionservice
from readanno.views import jobs
from readanno.views import calibrate
from readanno.views import read
from readanno.views import time1, time2, time3, outcome
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
                       url(r'^time1/(\d{1,2})/$', time1),
                       url(r'^time2/(\d{1,2})/$', time2),
                       url(r'^time3/(\d{1,2})/$', time3),
                       url(r'^outcome/(\d{1,2})/$', outcome),

                       url(r'^docservice/(\d{1,2})/(\d{1,2})/$', docservice),
                       url(r'^docquestionservice/(\d{1,2})/(\d{1,2})/$', docquestionservice),
                       url(r'^docoptionservice/(\d{1,2})/(\d{1,2})/$', docoptionservice),

                       url(r'^LogService/$', log)
                       )
