from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns(
    '',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^project/new', create_project, name='project-new'),
    url(r'^project/(?P<pk>\d+)/edit', EditProject.as_view(), name='project-edit'),
    url(r'^project/(?P<pk>\d+)$', ProjectDetailView.as_view(), name='project-detail'),
    url(r'^person/(?P<pk>\d+)$', PersonDetailView.as_view(), name='person-detail'),
    url(r'^task/new$', create_task, name='task-new'),
    url(r'^get_users$', get_users, name='get-users'),
)