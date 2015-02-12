from django.forms import Form, ModelForm
from pm.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'requester', 'description', 'start_date', 'due_date']