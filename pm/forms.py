from django import forms
from pm.models import Project, People, Task, Worker, TaskDependency
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "create_project"
        self.helper.form_action = "project-new"
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Div(
                Div(Field('name'), css_class='col-sm-6'),
                Div(Field('requester'), css_class='col-sm-3'),
                Div(Field('project_manager'), css_class='col-sm-3'),
                css_class='row',
            ),
            Div(
                Div(Field('description'), css_class='col-sm-8'),
                Div(
                    Div(
                        Div(Field('start_date'), css_class='col-sm-12 datemask'),
                        Div(Field('due_date'), css_class='col-sm-12 datemask'),
                        Div(Field('date_complete'), css_class='col-sm-12 datemask'),
                        css_class='row',
                    ),
                    css_class='col-sm-4',
                ),
                css_class='row',
            ),
            Div(
                Div(Field('program'), css_class='col-sm-2'),
                Div(Field('status'), css_class='col-sm-2'),
                Div(Field('priority'), css_class='col-sm-2'),
                Div(Field('sharepoint_ticket'), css_class='col-sm-6'),
                css_class='row',
            )
        )

    class Meta:
        model = Project


class TaskForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label=None)
    name = forms.CharField()
    start_date = forms.DateField()
    due_date = forms.DateField(required=False)
    status = forms.ChoiceField(choices=Task.STATUS_CHOICES)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 60}), required=False)
    worker = forms.ModelMultipleChoiceField(queryset=Worker.objects.none())
    blocked_by = forms.ModelMultipleChoiceField(queryset=Task.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        self.project_id = kwargs.pop('project_id')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['worker'].queryset = Worker.objects.filter(project=self.project_id)
        self.fields['blocked_by'].queryset = Task.objects.filter(project=self.project_id)

        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.form_id = "create-task"
        self.helper.form_action = "task-new"
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Div(
                Div(Field('name'), css_class='col-lg-3 col-sm-6'),
                Div(Field('start_date'), css_class='col-lg-3 col-sm-6'),
                Div(Field('due_date'), css_class='col-lg-3 col-sm-6'),
                Div(Field('status'), css_class='col-lg-3 col-sm-6'),
                css_class='row',
            ),
            Div(
                Div(Field('description'), css_class='col-lg-3 col-sm-6'),
                Div(Field('worker'), css_class='col-lg-3 col-sm-6'),
                Div(Field('blocked_by'), css_class='col-lg-3 col-sm-6'),
                Div(Field('project'), css_class='col-lg-3 col-sm-6'),
                css_class='row',
            ),
        )

