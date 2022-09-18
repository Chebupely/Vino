from django.db import models

class Info(models.Model):
    vino = models.CharField('Виноградники', max_length=255)
    height = models.CharField('Высота', max_length=255)
    aspect = models.CharField('Экспозиция', max_length=255)
    slope = models.CharField('Уклон', max_length=255)
    water = models.CharField('Затопляемость', max_length=255)

    def _str_(self):
        return self.title