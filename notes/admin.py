from django.contrib import admin
from .models import Note, Project


class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    fields = ('user', 'project', 'references', 'text')

admin.site.register(Note, NoteAdmin)
admin.site.register(Project)
