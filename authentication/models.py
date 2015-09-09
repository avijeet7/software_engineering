from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserType(models.Model):
    UserId = models.ForeignKey(User)
    Type = models.CharField(max_length=1, default="S")
