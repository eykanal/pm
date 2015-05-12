from datetime import date, timedelta
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models


# Redefine the User model to use a cleaner name rather than the
# username itself, which may be difficult to interpret
def user_unicode_patch(self):
    return u'%s, %s (%s)' % (self.last_name, self.first_name, self.username)

User.__unicode__ = user_unicode_patch


class Group(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    internal = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class People(models.Model):
    name = models.OneToOneField(settings.AUTH_USER_MODEL)
    group = models.ForeignKey(Group)

    class Meta:
        unique_together = ('name', 'group',)
        permissions = (
            ('view_people', 'Can view people'),
            ('modify_people', 'Can create, edit, and delete people'),
        )

    def __unicode__(self):
        return "%s, %s (%s)" % (self.name.last_name, self.name.first_name, self.group.name)

    def full_name(self):
        return "%s %s" % (self.name.first_name, self.name.last_name)
        
    def full_name_lastnamefirst(self):
        return "%s, %s" % (self.name.last_name, self.name.first_name)
    
    def lead_count(self):
        return self.worker_set.filter(owner=True).count()

    def task_count(self):
        return TaskWorker.objects.filter(worker__person=self).count()

    def two_wk_task_count(self):
        return TaskWorker.objects.filter(worker__person=self, task__due_date__range=[
            date.today(),
            date.today() + timedelta(14)
        ]).count()


class Program(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        permissions = (
            ('modify_program', 'Can create, edit, and delete programs'),
        )

    def __unicode__(self):
        return self.name


class Project(models.Model):
    HIGH = 'HI'
    STANDARD = 'ST'
    LOW = 'LO'
    PRIORITY_CHOICES = (
        (HIGH, 'High'),
        (STANDARD, 'Standard'),
        (LOW, 'Low')
    )

    ACTIVE = 'A'
    ON_HOLD = 'O'
    WARRANTY = 'W'
    MAINTENANCE = 'M'
    COMPLETED = 'C'
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (ON_HOLD, 'On hold'),
        (WARRANTY, 'Warranty'),
        (MAINTENANCE, 'Maintenance'),
        (COMPLETED, 'Completed')
    )

    name = models.CharField(max_length=500)
    requester = models.ForeignKey(People, related_name="person_requester")
    project_manager = models.ForeignKey(People, related_name="person_project_manager")
    program = models.ForeignKey(Program)
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    date_complete = models.DateField(null=True, blank=True)
    sharepoint_ticket = models.URLField(null=True, blank=True)
    priority = models.CharField(null=True, choices=PRIORITY_CHOICES, default=STANDARD, max_length=2)
    status = models.CharField(choices=STATUS_CHOICES, default=ACTIVE, max_length=1)

    class Meta:
        permissions = (
            ('view_project', 'Can view projects'),
            ('modify_project', 'Can create, edit, and delete projects'),
        )

    def __unicode__(self):
        return self.name

    def completed_tasks(self):
        """
        Return the number of completed tasks in a project.
        """
        return self.task_set.exclude(date_complete=None)

    def est_completion_date(self):
        """
        Iterate through the tasks in a project, return the latest due date as
        the project completion estimate. If no tasks are yet assigned, return
         "No Estimate".
        """
        if self.task_set.all().count() is 0:
            return "No estimate"
        else:
            due_dates = []
            for task in self.task_set.all():
                if task.due_date is None:
                    continue
                else:
                    due_dates.append(task.due_date)
            if len(due_dates) == 0:
                return "No estimate"
            else:
                return max(due_dates)
    
    def next_tasks(self):
        """
        Return a list of the next tasks due plus due dates.
        """
        due_date_list = self.task_set.exclude(due_date=None).values('due_date')  # min() returns a dict, pulling the datetime value out
        if not due_date_list:
            return due_date_list
        next_due_date = min(due_date_list)['due_date'] 
        return self.task_set.filter(due_date=next_due_date)


class Worker(models.Model):
    project = models.ForeignKey(Project)
    person = models.ForeignKey(People)
    date_added = models.DateField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    date_complete = models.DateField(null=True, blank=True)
    percent_committed = models.IntegerField(null=True, blank=True)
    owner = models.BooleanField(default=False)

    class Meta:
        unique_together = ('project', 'person',)

    def __unicode__(self):
        return "%s (%s) - %s" % (self.person.full_name(), self.person.group.name, self.project.name)


class Task(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=500)
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    date_complete = models.DateField(null=True, blank=True)
    status_on_hold = models.BooleanField(default=False)
    status_waiting = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'project',)
        permissions = (
            ('view_task', 'Can view tasks'),
            ('modify_task', 'Can create, edit, and delete tasks'),
        )

    def __unicode__(self):
        return "%s - %s" % (self.name, self.project.name)

    def status(self):
        if self.date_complete is not None:
            return 'Complete'
        elif TaskDependency.objects.filter(blocked_task=self).filter(blocking_task__date_complete=None).exists():
            return 'Queued'
        elif self.status_waiting:
            return 'Waiting on\n external party'
        elif self.status_on_hold:
            return 'On hold'
        else:
            return 'Active'


class TaskDependency(models.Model):
    blocking_task = models.ForeignKey(Task, related_name="blocking_task")
    blocked_task = models.ForeignKey(Task, related_name="blocked_task")

    class Meta:
        unique_together = ('blocking_task', 'blocked_task',)

    def __unicode__(self):
        return "%s - %s" % (self.blocking_task, self.blocked_task)


class TaskWorker(models.Model):
    task = models.ForeignKey(Task)
    worker = models.ForeignKey(Worker)

    class Meta:
        unique_together = ('task', 'worker',)

    def __unicode__(self):
        return "%s (%s) - %s - %s" % (self.worker.person.full_name(), self.worker.person.group.name, self.worker.project.name, self.task.name)
