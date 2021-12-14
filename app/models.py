from django.db import models

class UserInputModel(models.Model):
    start = models.DateField(null=False)
    end = models.DateField(null=False)
    latitude = models.FloatField(null=False)
    longititude = models.FloatField(null=False)