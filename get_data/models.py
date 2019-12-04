from django.db import models

class UserInput(models.Model):
    proteins = models.IntegerField(max_length = 4)
    carbohydrates = models.IntegerField(max_length = 4)
    fat = models.IntegerField(max_length = 4)
    calories = models.IntegerField()
