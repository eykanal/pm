import json

from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
from django.db.models import Q
from pm.models import Project, People
from pm.forms import ProjectForm


# template preprocessor function - people & projects always needed for sidebar
def menu_items(request):
    return {
        'projects': Project.objects.all().order_by('name'),
        'people': People.objects.filter(Q(group="MAAD") | Q(group="OAR")).order_by('name')
    }


# Main view
class Index(TemplateView):
    template_name = "pm/index.html"


class ProjectDetailView(DetailView):
    model = Project
    template_name = "pm/project_detail.html"

    def get_context_data(self, **kwargs):
            kwargs['project'] = kwargs['object']
            del kwargs['object']
            return super(ProjectDetailView, self).get_context_data(**kwargs)


class PersonDetailView(DetailView):
    model = People
    template_name = "pm/person_detail.html"

    def get_context_data(self, **kwargs):
            kwargs['person'] = kwargs['object']
            del kwargs['object']
            return super(PersonDetailView, self).get_context_data(**kwargs)


# handle form submission for new project
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"result": "success"})
        else:
            form.errors["result"] = "fail"
            return JsonResponse(form.errors)


class CreateProject(CreateView):
    form_class = ProjectForm
    model = Project
    template_name = "pm/project_new.html"


class EditProject(UpdateView):
    pass

