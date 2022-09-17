from django.db import models
# Create your models here.


class Vinogradnik(models.Model):
    name_Vinogradnik = models.CharField(max_length=150)
    number_Vinogradnik = models.IntegerField()
    shirota_Vinogradnik = models.CharField(max_length=15)
    dolgota_Vinogradnik = models.CharField(max_length=15)
    description_Vinogradnik = models.CharField(max_length=350)
    image_Vinogradnik = models.ImageField()


def __str__(self):
    return self.name


class Vinograd(models.Model):
    vinogradnik = models.ForeignKey(Vinogradnik, on_delete=models.DO_NOTHING)
    name_Vinograd = models.CharField(max_length=150)
    description_Vinogradnik = models.CharField(max_length=350)
    image_Vinogradnik = models.ImageField()


def __str__(self):
    return self.name