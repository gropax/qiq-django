from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
import notes
import core.utils
#from notes.helpers import age
#import notes.helpers


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL,
                                related_name='notes', blank=True, null=True)

    text = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    references = models.ManyToManyField('self', db_table='references', symmetrical=False,
                                        related_name='referencers')
    rank = models.IntegerField(default=1)
    original = models.BooleanField(default=True)

    def __str__(self):
        l = len(self.text)
        return self.text[:50] + ('...' if l > 50 else '')

    def age(self):
        return core.utils.age(self.created)


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE,
                             related_name='documents')

    name = models.CharField(max_length=32, blank=False)
    description = models.CharField(max_length=80, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def age(self):
        return core.utils.age(self.created)

    class Meta:
        unique_together = ('user', 'name')
