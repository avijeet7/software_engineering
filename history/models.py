from django.db import models

class StudentHistory(models.Model):
	roll_no = models.CharField(max_length=10)

class StudentCourses(models.Model):
	user = models.ForeignKey(StudentHistory)
	course = models.CharField(max_length=10)