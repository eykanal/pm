from rest_framework import serializers
from pm.models import Group, Program, Project, People, Worker, Task, TaskWorker, TaskDependency
from django.contrib.auth.models import User


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('id', 'name', 'manager', 'internal')


class ProgramSerializer(serializers.ModelSerializer):
	class Meta:
		model = Program
		fields = ('id', 'name', 'description', 'date_added')


class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = ('id', 'name', 'requester', 'project_manager', 'program', 'description', 'date_added', 'start_date', 'due_date', 'date_complete', 'sharepoint_ticket', 'priority', 'status')


class PeopleSerializer(serializers.ModelSerializer):
	class Meta:
		model = People
		fields = ('id', 'name', 'group')


class WorkerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Worker
		fields = ('project', 'person', 'date_added', 'start_date', 'date_complete', 'percent_committed', 'owner')


class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = ('project', 'name', 'description', 'date_added', 'start_date', 'due_date', 'date_complete', 'status_on_hold', 'status_waiting')


class TaskWorkerSerializer(serializers.ModelSerializer):
	class Meta:
		model = TaskWorker
		fields = ('id', 'task', 'worker')


class TaskDependencySerializer(serializers.ModelSerializer):
	class Meta:
		model = TaskDependency
		fields = ('id', 'blocking_task', 'blocked_task')

