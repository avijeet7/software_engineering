from django.db import models
from course.models import Catalog

from django.contrib.auth.models import User

class Student(models.Model):
    UserId = models.ForeignKey(User)
    rollno = models.CharField(max_length=15)
    department = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.rollno) + ": " + str(self.department)

class StudentCourses(models.Model):
    UserId = models.ForeignKey(User)
    courseid = models.ForeignKey(Catalog)
    enroll_limit_status_inst = models.CharField(max_length=10,default="W")
    enroll_limit_status_reg = models.CharField(max_length=10,default="A")
    class Meta:
        unique_together = ('UserId', 'courseid')

