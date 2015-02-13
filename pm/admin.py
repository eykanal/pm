from django.contrib import admin
from pm.models import People, Group, Project, Worker, Task, TaskWorker


class PeopleInline(admin.TabularInline):
    model = People
    extra = 3
    ordering = ('name',)


class GroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']})
    ]
    inlines = [PeopleInline]


class WorkerInline(admin.TabularInline):
    model = Worker
    extra = 3


class ProjectAdmin(admin.ModelAdmin):
    inlines = [WorkerInline]


class TaskWorkerInline(admin.TabularInline):
    model = TaskWorker
    extra = 3


class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskWorkerInline]


admin.site.register(People)
admin.site.register(Group, GroupAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Worker)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskWorker)
