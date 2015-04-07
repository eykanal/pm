from django.contrib import admin
from pm.models import People, Group, Program, Project, Worker, Task, TaskWorker, TaskDependency


class PeopleInline(admin.TabularInline):
    model = People
    extra = 3
    ordering = ('name',)


class GroupAdmin(admin.ModelAdmin):
    inlines = [PeopleInline]
    list_display = ('name', 'manager', 'internal')


class WorkerInline(admin.TabularInline):
    model = Worker
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    inlines = [WorkerInline]
    list_display = ('name', 'requester', 'project_manager', 'program', 'date_added', 'start_date', 'due_date', 'date_complete', 'priority', 'status')


class TaskDependencyInline(admin.TabularInline):
    model = TaskDependency
    extra = 2
    fk_name = 'blocking_task'


class TaskDependencyInline2(admin.TabularInline):
    model = TaskDependency
    extra = 2
    fk_name = 'blocked_task'


class TaskWorkerInline(admin.TabularInline):
    model = TaskWorker
    extra = 3


class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskWorkerInline, TaskDependencyInline]
    list_display = ('name', 'project', 'date_added', 'start_date', 'due_date', 'date_complete', 'status')


admin.site.register(People)
admin.site.register(Group, GroupAdmin)
admin.site.register(Program)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
