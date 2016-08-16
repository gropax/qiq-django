from django.db import models


class Note(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        l = len(self.text)
        return self.text[:50] + ('...' if l > 50 else '')
