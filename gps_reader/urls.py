from django.conf.urls import patterns, include, url

urlpatterns = patterns('gps_reader.views',
    url(r'^$', 'index'),
    url(r'^(?P<activity_id>\d+)/$', 'detail', name='activityDetail'),
    url(r'^upload/$', 'upload'),
)
