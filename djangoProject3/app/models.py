from django.db import models

# Create your models here.
class Registeruser(models.Model):
    reg_name = models.CharField(max_length=100, unique=False)
    reg_pwd= models.CharField(max_length=100, unique=False)