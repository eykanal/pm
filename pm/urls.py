# myapp/urls
from django.conf.urls import patterns, url
from pm import views
from views import *


urlpatterns = patterns(
    '',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^create_project$', create_project, name='create_project'),
    url(r'^create_project_2$', CreateProject.as_view(), name='create_project_2')
)