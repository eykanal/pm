import json

from django.http import JsonResponse
from django.views.generic import TemplateView, UpdateView, CreateView
from pm.models import Project, People
from pm.forms import ProjectForm


# template preprocessor function - people & projects always needed for sidebar
def menu_items(request):
    return {
        'projects': Project.objects.all(),
        'people': People.objects.all()
    }


# Main view
class Index(TemplateView):
    projects = Project.objects.all()
    proj_form = ProjectForm()
    template_name = "pm/index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context.update({
            'projects': self.projects,
            'proj_form': self.proj_form,
        })
        return context


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
