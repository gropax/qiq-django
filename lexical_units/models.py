from django.db import models
from django.contrib.auth.models import User
from languages.models import Language
import core.utils

class LexicalUnit(models.Model):
    NA = 0
    NOUN = 10
    VERB = 20
    ADJECTIVE = 30
    ADVERB = 40

    GRAMMATICAL_CATEGORIES = (
        (NA, "-"),
        (NOUN, "N"),
        (VERB, "V"),
        (ADJECTIVE, "ADJ"),
        (ADVERB, "ADV"),
    )
    GRAMMATICAL_CATEGORIES_DICT = {k: v for k, v in GRAMMATICAL_CATEGORIES}
    CATEGORIES = [c for _, c in GRAMMATICAL_CATEGORIES[1:]]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 related_name='lexical_units')

    category = models.SmallIntegerField(choices=GRAMMATICAL_CATEGORIES, default=NA)
    lemma = models.CharField(max_length=80)
    created = models.DateTimeField(auto_now_add=True)

    def age(self):
        return core.utils.age(self.created)

    @property
    def grammatical_category(self):
        return self.__class__.GRAMMATICAL_CATEGORIES_DICT[self.category]

    @grammatical_category.setter
    def grammatical_category(self, cat):
        cat_id = None
        for i, c in self.__class__.GRAMMATICAL_CATEGORIES:
            if cat == c:
                cat_id = i

        if cat_id:
            self.category = cat_id
            self.save()
        else:
            raise ValueError("Unknown category: `%s`" % cat)

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
