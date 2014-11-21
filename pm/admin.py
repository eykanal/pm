from django.contrib import admin
from pm.models import People, Group, Project


class PeopleInline(admin.TabularInline):
	model = People
	extra = 3
	ordering = ('name',)


class GroupAdmin(admin.ModelAdmin):
	fieldsets = [
		( None, {'fields': ['name']} )
	]
	inlines = [ PeopleInline ]


admin.site.register(People)
admin.site.register(Group, GroupAdmin)
admin.site.register(Project)