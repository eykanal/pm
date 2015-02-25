from datetime import date, timedelta
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __unicode__(self):
        return self.name


class People(models.Model):
    name = models.CharField(max_length=200)
    group = models.ForeignKey(Group)

    class Meta:
        unique_together = ('name', 'group',)

    def __unicode__(self):
        return ("%s-%s" % (self.name, self.group.name)).replace(" ", "_")

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
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    date_complete = models.DateField(null=True, blank=True)
    sharepoint_ticket = models.URLField(null=True, blank=True)
    priority = models.CharField(null=True, choices=PRIORITY_CHOICES, default=STANDARD, max_length=2)
    status = models.CharField(choices=STATUS_CHOICES, default=ACTIVE, max_length=1)
    program = models.ForeignKey(Program)

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
        due_date_list = self.task_set.values('due_date')  # min() returns a dict, pulling the datetime value out
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
        return ("%s-%s" % (self.person.name, self.project.name)).replace(" ", "_")


class Task(models.Model):
    QUEUED = 'Q'
    ACTIVE = 'A'
    ON_HOLD = 'O'
    WAITING = 'W'
    COMPLETED = 'C'
    STATUS_CHOICES = (
        (QUEUED, 'Queued'),
        (ACTIVE, 'Active'),
        (ON_HOLD, 'On hold'),
        (WAITING, 'Waiting on customer'),
        (COMPLETED, 'Completed')
    )

    project = models.ForeignKey(Project)
    name = models.CharField(max_length=500)
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    date_complete = models.DateField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default=QUEUED, max_length=1)

    class Meta:
        unique_together = ('name', 'project',)

    def __unicode__(self):
        return ("%s-%s" % (self.project.name, self.name)).replace(" ", "_")


class TaskDependency(models.Model):
    blocking_task = models.ForeignKey(Task, related_name="blocking_task")
    blocked_task = models.ForeignKey(Task, related_name="blocked_task")

    class Meta:
        unique_together = ('blocking_task', 'blocked_task',)

    def __unicode__(self):
        return ("%s-%s" % (self.blocking_task, self.blocked_task)).replace(" ", "_")


class TaskWorker(models.Model):
    task = models.ForeignKey(Task)
    worker = models.ForeignKey(Worker)

    class Meta:
        unique_together = ('task', 'worker',)

    def __unicode__(self):
        return ("%s-%s-%s" % (self.worker.person.name, self.worker.project.name, self.task.name)).replace(" ", "_")
