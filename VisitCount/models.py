from django.db import models

class Visitor(models.Model):
    count = models.PositiveIntegerField(default=0, verbose_name='গনণা')

    def __str__(self):
        return f'{self.count}'
    
    class Meta:
        verbose_name_plural = 'ওয়েবসাইট ভিজিট গনণা'