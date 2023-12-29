from django.db import models
import json

class VerbFormManager(models.Manager):
    def create(self, **extra_fields):
        verb = self.model(**extra_fields)
        verb.save()
        return verb


class VerbForm(models.Model):
    original = models.CharField(max_length=100, verbose_name='original verb')
    translation = models.CharField(max_length=1024, default='', verbose_name='translation')
    is_regular = models.BooleanField(default=False, verbose_name='if the verb is "regelmäßig"')
    is_separable = models.BooleanField(null=True, verbose_name='if the verb is "trennbar"')
    past_form = models.CharField(max_length=100, verbose_name='präteritum form')
    participle = models.CharField(max_length=100, verbose_name='partizip 2 form')
    level = models.CharField(max_length=5, verbose_name='on which level this word should be learned')
    created_at = models.DateTimeField(auto_now=True, verbose_name='this word was created at')

    objects = VerbFormManager()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __str__(self):
        if self.is_regular:
            reg_str = 'regelmäßig'
        else:
            reg_str = 'unregelmäßig'
        return f'{self.level} * {reg_str} | {self.original} - {self.past_form} - {self.participle}\n{self.translation}'
