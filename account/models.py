from django.db import models
from django.utils import timezone
from datetime import datetime
# Create your models here.
class offerride(models.Model):
    userid=models.CharField(max_length=100)
    startingpoint = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    datetime  = models.DateTimeField(default=datetime.now,blank=True)
    vacancy = models.IntegerField()
    phonenumb = models.CharField(max_length=10)
    passenger1=models.CharField(max_length=100,default=None)
    passenger2=models.CharField(max_length=100,default=None)
    passenger3=models.CharField(max_length=100,default=None)
    passenger4=models.CharField(max_length=100,default=None)
    passenger5=models.CharField(max_length=100,default=None)
    passenger6=models.CharField(max_length=100,default=None)