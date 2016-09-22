from django.db import models


class Language(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=32)
