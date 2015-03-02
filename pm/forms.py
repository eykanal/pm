from django import forms
from django.forms import Form, ModelForm
from pm.models import Project, People, Task, Worker, TaskDependency
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "create_project"
        self.helper.form_action = "project-new"
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Project
        fields = ['name', 'requester', 'description', 'start_date', 'due_date']


class TaskForm(Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    name = forms.CharField()
    start_date = forms.DateField()
    due_date = forms.DateField()
    status = forms.ChoiceField(choices=Task.STATUS_CHOICES)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 60}))
    worker = forms.ModelMultipleChoiceField(queryset=Worker.objects.none())
    dependencies = forms.ModelMultipleChoiceField(queryset=TaskDependency.objects.none())

    def __init__(self, *args, **kwargs):
        self.project_id = kwargs.pop('project_id')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['worker'].queryset = People.objects.filter(worker__project=self.project_id)

        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.form_id = "create-task"
        self.helper.form_action = "task-new"
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Div(
                Div(Field('name'), css_class='col-md-3'),
                Div(Field('start_date'), css_class='col-md-3'),
                Div(Field('due_date'), css_class='col-md-3'),
                Div(Field('status'), css_class='col-md-3'),
                css_class='row',
            ),
            Div(
                Div(Field('description'), css_class='col-md-6'),
                Div(Field('worker'), css_class='col-md-3'),
                Div(Field('dependencies'), css_class='col-md-3'),
                css_class='row',
            )
        )

