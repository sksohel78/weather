from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, default='')
    last_name = models.CharField(max_length=50, blank=True, default='')

class Location(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    point = models.PointField(null=True, blank=True, spatial_index=True, geography=True)
    office = models.CharField(max_length=50, null=True, blank=True)
    grid_x = models.IntegerField(default=0, null=True, blank=True)
    grid_y = models.IntegerField(default=0, null=True, blank=True)

