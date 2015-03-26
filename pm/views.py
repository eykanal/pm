import json

from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from pm.models import Program, Project, People, Task, Worker, TaskWorker, TaskDependency
from pm.forms import ProjectForm, TaskForm
from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form


# template preprocessor function - people & projects always needed for sidebar
def menu_items(request):
    if 'pm' in request.resolver_match.namespaces:
        return {
            'projects': Project.objects.all().order_by('name'),
            'people': People.objects.filter(Q(group="MAAD") | Q(group="OAR")).order_by('name')
        }
    return {}

# Main view
class Index(TemplateView):
    template_name = "pm/index.html"


class ProjectDetailView(DetailView):
    model = Project
    template_name = "pm/project_detail.html"

    def get_context_data(self, **kwargs):
            kwargs['project'] = kwargs['object']
            del kwargs['object']
            kwargs['taskform'] = TaskForm(project_id=self.kwargs['pk'], initial={'project': self.kwargs['pk']})
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


# create new task via AJAX
@json_view
def create_task(request):
    pk = request.POST['project']
    form = TaskForm(request.POST, project_id=pk)
    if form.is_valid():

        # save task itself
        t = Task(
            project=form.cleaned_data['project'],
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            start_date=form.cleaned_data['start_date'],
            due_date=form.cleaned_data['due_date'],
            status=form.cleaned_data['status'])
        t.save()

        # save workers
        for w in form.cleaned_data['worker']:
            print w
            tw = TaskWorker(
                task=Task.objects.get(pk=t.id),
                worker=w
            )
            tw.save()

        # save dependencies
        for d in form.cleaned_data['blocked_by']:
            td = TaskDependency(
                blocking_task=d,
                blocked_task=Task.objects.get(pk=t.id)
            )
            td.save()

        return {'success': True}

    form_html = render_crispy_form(form, context=RequestContext(request))
    return {'success': False, 'form_html': form_html}


def create_project(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            # save project
            # save workers
            # return to project page
            return Index()
        else:
            # handle errors
            pass
    else:
        form = ProjectForm(initial={'program': Program.objects.get(name="None")})

    return render_to_response("pm/project_new.html", {'form': form}, context)


class EditProject(UpdateView):
    pass

