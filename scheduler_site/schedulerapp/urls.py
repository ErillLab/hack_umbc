from django.conf.urls import patterns, url

urlpatterns = patterns('schedulerapp.views',
    url(r'^home/$', 'home'),
    url(r'^list_all_courses/$', 'list_all_courses'),
)
