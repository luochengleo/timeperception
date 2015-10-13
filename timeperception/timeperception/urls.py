from django.conf.urls import patterns, include, url
from django.contrib import admin
from readanno.views import login
from readanno.views import tasks
from readanno.views import calibrate
from readanno.views import read
from readanno.views import feedback

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'timeperception.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/$', login),
                       url(r'^tasks/(\d{1,2})/$', tasks),
                       url(r'^calibrate/(\d{1,2})/$', calibrate),
                       url(r'^read/(\d{1,2})/(\d{1,2})/$', read),
                       url(r'^feedback/(\d{1,2})/$', feedback)
                       )
