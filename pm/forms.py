from django.forms import Form, ModelForm
from pm.models import Project
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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


class TaskForm(ModelForm):
    pass