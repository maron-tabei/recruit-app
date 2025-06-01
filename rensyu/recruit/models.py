from django.db import models
from datetime import date

# Create your models here.

class Recruit(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    entry_day = models.DateField(default=date.today)
    documents_status = models.CharField(max_length=100)

