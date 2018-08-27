from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    calories = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Meal(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    foods = models.ManyToManyField(Food)
