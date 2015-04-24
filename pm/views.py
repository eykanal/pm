import json

from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from pm.models import Program, Project, Group, People, Task, Worker, TaskWorker, TaskDependency
from pm.forms import ProjectForm, TaskForm
from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form


# template preprocessor function - people & projects always needed for sidebar
def menu_items(request):
    if 'pm' in request.resolver_match.namespaces:
        return {
            'internal_groups': Group.objects.filter(internal=True),
            'projects': Project.objects.all().order_by('name'),
            'peoples': People.objects.filter(group__internal=True).order_by('name__last_name')
        }
    return {}


# Mixin for Class-Based Views to enable login_required functionality
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


# Main view
class Index(LoginRequiredMixin, TemplateView):
    template_name = "pm/index.html"


@login_required()
def project_detail(request, pk):
    context = RequestContext(request)
    project = Project.objects.get(pk=pk)
    taskform = TaskForm(project_id=pk, initial={'project': pk})
    return render_to_response("pm/project_detail.html", {'project': project, 'taskform': taskform}, context)


class PersonDetailView(LoginRequiredMixin, DetailView):
    model = People
    template_name = "pm/person_detail.html"

    def get_context_data(self, **kwargs):
            kwargs['person'] = kwargs['object']
            del kwargs['object']
            return super(PersonDetailView, self).get_context_data(**kwargs)


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

        # save workers (note that "w" here is a Person, not a Worker)
        for w in form.cleaned_data['worker']:
            tw = TaskWorker(
                task=Task.objects.get(pk=t.id),
                worker=Worker.objects.get(person=w, project=form.cleaned_data['project']),
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


@login_required()
def create_project(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            p = Project(
                name=form.cleaned_data['name'],
                requester=form.cleaned_data['requester'],
                project_manager=form.cleaned_data['project_manager'],
                program=form.cleaned_data['program'],
                description=form.cleaned_data['description'],
                start_date=form.cleaned_data['start_date'],
                due_date=form.cleaned_data['due_date'],
                date_complete=form.cleaned_data['date_complete'],
                sharepoint_ticket=form.cleaned_data['sharepoint_ticket'],
                priority=form.cleaned_data['priority'],
                status=form.cleaned_data['status'])
            p.save()

            for w in form.cleaned_data['workers']:
                w = Worker(
                    project=Project.objects.get(pk=p.id),
                    person=w,
                )
                w.save()

            return redirect('pm:index')
        else:
            # handle errors
            print form.cleaned_data
            pass
    else:
        form = ProjectForm(initial={'program': Program.objects.get(name="None")})

    return render_to_response("pm/project_new.html", {'form': form}, context)


@json_view()
def get_users(request):
    print request.GET['q']
    response = []
    everyone = People.objects.filter(Q(name__first_name__contains=request.GET['q']) | Q(name__last_name__contains=request.GET['q']))
    for p in everyone:
        response.append({"id": p.pk, "text": p.full_name()})
    # return {'items': [{'id': 'bob', 'text': 'joe'}, {'id': 'frank', 'text': 'me'}]}
    return {'items': response}


class EditProject(LoginRequiredMixin, UpdateView):
    pass
