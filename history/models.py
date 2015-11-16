from django.db import models
from django.contrib.auth.models import User


class StudentCourseHistory(models.Model):
	user = models.ForeignKey(User)
	course = models.CharField(max_length=10)