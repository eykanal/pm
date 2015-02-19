from django.conf.urls import patterns, url
from pm import views
from views import *

# TODO: create project detail view
# TODO: create people detail view
urlpatterns = patterns(
    '',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^create_project$', create_project, name='create_project'),
    url(r'^create_project_2$', CreateProject.as_view(), name='create_project_2'),
    url(r'^project/(?P<pk>\d+)$', ProjectDetailView.as_view(), name='project-detail'),
    url(r'^person/(?P<pk>\d+)$', PersonDetailView.as_view(), name='person-detail'),
)