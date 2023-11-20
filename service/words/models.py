from django.db import models


class VerbForm(models.Model):
    original = models.CharField(max_length=100, verbose_name='original verb')
    translation = models.CharField(max_length=1024, default='', verbose_name='translation')
    is_regular = models.BooleanField(default=False, verbose_name='if the verb is "regelmäßig"')
    past_form = models.CharField(max_length=100, verbose_name='präteritum form')
    participle = models.CharField(max_length=100, verbose_name='partizip 2 form')
    level = models.CharField(max_length=5, verbose_name='on which level this word should be learned')
    created_at = models.DateTimeField(auto_now=True, verbose_name='this word was created at')

    def __str__(self):
        if self.is_regular:
            reg_str = 'regelmäßig'
        else:
            reg_str = 'unregelmäßig'
        return f'{self.level} * {reg_str} | {self.original} - {self.past_form} - {self.participle}\n{self.translation}'
