from django.db import models
from django.contrib.auth.models import User
from languages.models import Language
import core.utils


class LexicalUnit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 related_name='lexical_units')

    #category = models.CharField(max_length=80)
    lemma = models.CharField(max_length=80)
    created = models.DateTimeField(auto_now_add=True)

    def age(self):
        return core.utils.age(self.created)

    class Meta:
        unique_together = ('user', 'language', 'lemma')


class LexicalPattern(models.Model):
    lexical_unit = models.ForeignKey(LexicalUnit, on_delete=models.CASCADE,
                                     related_name='patterns')

    description = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def age(self):
        return core.utils.age(self.created)


#class LexicalFunction(models.Model):
    #pass
