from django.db import models

# Create your models here.

class Paper(models.Model):
    title = models.CharField(max_length=100)
    abstract = models.CharField(max_length=600)