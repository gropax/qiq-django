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
