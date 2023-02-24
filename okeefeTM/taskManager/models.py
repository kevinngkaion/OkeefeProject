from django.db import models

# Create your models here.
class Department(models.Model):
  dep_name = models.CharField(max_length=30)

class Category(models.Model):
  cat_name = models.CharField(max_length=30)