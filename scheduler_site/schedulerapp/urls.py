from django.conf.urls import patterns, url

urlpatterns = patterns('schedulerapp.views',
    url(r'^home/$', 'home'),
)
