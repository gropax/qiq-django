from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


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
