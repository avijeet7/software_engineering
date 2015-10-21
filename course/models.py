from django.db import models

# Create your models here.
class Catalog(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=40)
    instructor = models.CharField(max_length=40)
    credits = models.SmallIntegerField(default=0)
    coursetag = models.CharField(max_length=1,default="C")  #department elective or core course
    prereq = models.CharField(max_length=100,default="")
    def __str__(self):
        return str(self.code) + ": " + str(self.name) + " [" + str(self.credits) + "]"

