from django.db import models

# Create your models here.

class Urls(models.Model):
    orig =  models.CharField(max_length=128)
    acort =  models.CharField(max_length=128)
    def __str__(self):
        return "Url: " + self.orig + "; Url acortada: " + self.acort
