from django.db import models

# Create your models here.
class user(models.Model):
    username = models.CharField(max_length=99)
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=99, unique=True)
    password = models.CharField(max_length=99)
    contact = models.CharField(max_length=29)