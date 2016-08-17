from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               related_name='children', blank=True, null=True)

    name = models.CharField(max_length=32, blank=False)
    description = models.CharField(max_length=80, blank=True)

    def full_name(self):
        if self.parent:
            return self.parent.__str__() + '.' + self.name
        else:
            return self.name

    def __str__(self):
        return self.full_name()

    class Meta:
        unique_together = ('user', 'parent', 'name')


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
