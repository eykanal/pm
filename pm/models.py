from django.db import models


class Project(models.Model):
	name			= models.CharField(max_length=500)
	requester		= models.CharField(max_length=500)
	description		= models.TextField()
	date_added		= models.DateField(auto_now_add=True)
	start_date		= models.DateField()
	due_date		= models.DateField(null=True, blank=True)
	date_complete	= models.DateField(null=True, blank=True)

	def __unicode__(self):
		return self.name


class Group(models.Model):
	name			= models.CharField(max_length=200, primary_key=True)

	def __unicode__(self):
		return self.name


class People(models.Model):
	name			= models.CharField(max_length=200)
	group			= models.ForeignKey(Group)


	class Meta:
		unique_together = ('name', 'group',)

	def __unicode__(self):
		return self.name


class Worker(models.Model):
	project			= models.ForeignKey(Project)
	person			= models.ForeignKey(People)
	date_added		= models.DateField(auto_now_add=True)
	start_date		= models.DateField(null=True, blank=True)
	date_complete	= models.DateField(null=True, blank=True)
	percent_committed = models.IntegerField(null=True, blank=True)
	owner			= models.BooleanField(default=False)


	class Meta:
		unique_together = ('project', 'person',)

	def __unicode__(self):
		return ("%s-%s" % (self.person.name, self.project.name)).replace(" ", "_")


class Task(models.Model):
	name 			= models.CharField(max_length=500)
	project			= models.ForeignKey(Project)
	description		= models.TextField()
	date_added		= models.DateField(auto_now_add=True)
	start_date		= models.DateField(null=True, blank=True)
	due_date		= models.DateField(null=True, blank=True)
	date_complete	= models.DateField(null=True, blank=True)


	class Meta:
		unique_together = ('name', 'project')

	def __unicode__(self):
		return "%s-%s" % (self.project.name, name)


class TaskWorker(models.Model):
	task			= models.ForeignKey(Task)
	worker 			= models.ForeignKey(Worker)


	class Meta:
		unique_together = ('task', 'worker',)

	def __unicode__(self):
		return ("%s-%s-%s" % (self.worker.person.name, self.worker.project.name, self.task.name)).replace (" ", "_")
