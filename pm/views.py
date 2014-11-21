from django.views.generic import TemplateView
from pm.models import *

# Create your views here.
class Index(TemplateView):
	projects = Project.objects.all()
	template_name = "pm/index.html"

	def get_context_data(self, **kwargs):
		context = super(Index, self).get_context_data(**kwargs)
		context.update({'projects': self.projects})
		return context