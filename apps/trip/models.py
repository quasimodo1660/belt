from __future__ import unicode_literals
from django.db import models
from ..user.models import *

from datetime import datetime

class TripManager(models.Manager):
  def add_validator(self,post):
    errors = {}
    if len(post['des'])<1:
      errors['des']='Destination cannot be empty!'  
    if len(post['content'])<1:
      errors['content']='Description cannot be empty!'  
    dFrom=str(post['dFrom']).split('-')
    dTo=str(post['dTo']).split('-')
    if len(dFrom)==1 or len(dTo)==1:
      errors['dFrom']="Date cannot be empty!"
    else: 
      if datetime(int(dFrom[0]),int(dFrom[1]),int(dFrom[2]))>datetime(int(dTo[0]),int(dTo[1]),int(dTo[2])):
        errors['date']="Travel Date From must be before Travel Date To"
    return errors


class Trip(models.Model):
    place = models.CharField(max_length=255)
    content=models.TextField()
    date_to=models.DateField()
    date_from=models.DateField()
    user=models.ForeignKey(User,related_name='trips')
    join_user=models.ManyToManyField(User,related_name='joind_trips')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects=TripManager()