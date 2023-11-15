from django.db import models

class User(models.Model):
    identifier = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200, blank=True)
    surname = models.CharField(max_length=200, blank=True)