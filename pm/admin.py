from django.contrib import admin
from pm.models import People, Group, Project, Worker


class PeopleInline(admin.TabularInline):
    model = People
    extra = 3
    ordering = ('name',)


class GroupAdmin(admin.ModelAdmin):
    fieldsets = [
        ( None, {'fields': ['name']} )
    ]
    inlines = [ PeopleInline ]

class WorkerInline(admin.TabularInline):
    model = Worker
    extra = 3


admin.site.register(People)
admin.site.register(Group, GroupAdmin)
admin.site.register(Project)
admin.site.register(Worker)