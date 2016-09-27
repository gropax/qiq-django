from django.db import models
from django.contrib.auth.models import User
from languages.models import Language


class LexicalUnit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 related_name='lexical_units')

    #category = models.CharField(max_length=80)
    lemma = models.CharField(max_length=80)
    created = models.DateTimeField(auto_now_add=True)


class LexicalPattern(models.Model):
    lexical_unit = models.ForeignKey(LexicalUnit, on_delete=models.CASCADE,
                                     related_name='patterns')

    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)


#class LexicalFunction(models.Model):
    #pass
