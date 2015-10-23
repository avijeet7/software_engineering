from django.db import models

# Create your models here.
class Constraints(models.Model):
	min_credits = models.IntegerField(default=12)
	max_credits = models.IntegerField(default=30)
	max_enroll_limit_reg = models.IntegerField(default=10)
