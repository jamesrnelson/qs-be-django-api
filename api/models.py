from django.db import models

# Create your models here.
class Food(models.Model):
    """This class represents the food model."""
    name = models.CharField(max_length=255, blank=False, unique=True)
    calories = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
