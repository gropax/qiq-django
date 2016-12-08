from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
import notes
import core.utils


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL,
                                related_name='notes', blank=True, null=True)
    references = models.ManyToManyField('self', db_table='references', symmetrical=False,
                                        related_name='referencers')

    text = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    rank = models.IntegerField(default=1)
    original = models.BooleanField(default=True)

    def modify_text(self, text, time=None):
        self.text = text
        self.modified = time or timezone.now()
        self.save()

    def __str__(self):
        l = len(self.text)
        return self.text[:50] + ('...' if l > 50 else '')


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE,
                             related_name='documents')

    name = models.CharField(max_length=32, blank=False)
    description = models.CharField(max_length=80, blank=True, null=True)
    file = models.CharField(max_length=240, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def full_name(self):
        prj = self.note.project
        if prj:
            return prj.full_name() + '/' + self.name
        else:
            return self.name


    class Meta:
        unique_together = ('user', 'name')
