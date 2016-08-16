from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    references = models.ManyToManyField('self', db_table='references', symmetrical=False,
                                        related_name='referencers')

    def __str__(self):
        l = len(self.text)
        return self.text[:50] + ('...' if l > 50 else '')
