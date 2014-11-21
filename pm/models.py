from django.db import models


class Project(models.Model):
	name			= models.CharField(max_length=500)
	requester		= models.CharField(max_length=500)
	description		= models.TextField()
	date_added		= models.DateField(auto_now_add=True)
	start_date		= models.DateField()
	due_date		= models.DateField()
	date_complete	= models.DateField()

	def __unicode__(self):
		return self.name


class Group(models.Model):
	name			= models.CharField(max_length=200)

	def __unicode__(self):
		return self.name


class People(models.Model):
	name			= models.CharField(max_length=200)
	group			= models.ForeignKey(Group)

	def __unicode__(self):
		return self.name


class Worker(models.Model):
	project			= models.ForeignKey(Project)
	person			= models.ForeignKey(People)
	date_added		= models.DateField(auto_now_add=True)
	start_date		= models.DateField()
	date_complete	= models.DateField()
	percent_committed = models.IntegerField()
	owner			= models.BooleanField()

	def __unicode__(self):
		return ("%s-%s" % (self.person.name, self.project.name)).replace(" ", "_")


class Task(models.Model):
	name 			= models.CharField(max_length=500)
	project			= models.ForeignKey(Project)
	description		= models.TextField()
	date_added		= models.DateField(auto_now_add=True)
	start_date		= models.DateField()
	due_date		= models.DateField()
	date_complete	= models.DateField()

	def __unicode__(self):
		return "%s-%s" % (self.project.name, name)


class TaskWorker(models.Model):
	task			= models.ForeignKey(Task)
	worker 			= models.ForeignKey(Worker)

	def __unicode__(self):
		return ("%s-%s-%s" % (self.worker.person.name, self.worker.project.name, self.task.name)).replace (" ", "_")
