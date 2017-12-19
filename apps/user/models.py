from __future__ import unicode_literals
from django.db import models

import bcrypt
import re
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PSD_REGEX=re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{4,8}$')
PHONE_REGEX = re.compile(r'[0-9]{3}-[0-9]{3}-[0-9]{4}')
present=datetime.now()
NAME=re.compile(r'^[a-zA-Z]+$')




  # Create your models here.

class UserManager(models.Manager):
    def register_validator(self, postData):
      errors = {}
      if len(postData['fName'])<2 or not NAME.match(postData['fName']):
        errors['First_Name']='First name cannot fewer than 2 characters; letters only!' 
      if len(postData['lName'])<2 or not NAME.match(postData['lName']):
        errors['Last_Name']='last name cannot fewer than 2 characters; letters only!' 
      if len(postData['mail'].lower()) < 1:
        errors['Email']="Email cannot be blank!"
      if not PHONE_REGEX.match(postData['pnum']):
        errors['Phone']="Invalid Phone Number!"
      if not EMAIL_REGEX.match(postData['mail'].lower()):
        errors['Email']="Invalid Email Address!" 
      if not PSD_REGEX.match(postData['psd1']):
        errors['Password']="Invalid Password!"
      if postData['psd1']!=postData['psd2']:
        errors['Password']="Password should be the same!"
      dob=str(postData['dob']).split('-')       
      if len(dob)==1:
        errors['DOB']="DOB cannot be empty!"
      else:
          if datetime(int(dob[0]),int(dob[1]),int(dob[2]))>present:
            errors['DOB']="Invalid DOB!"
      if len(errors):
        return errors
      else:
        try:
          user=User.objects.get(email_address=postData['mail'].lower())
          errors['warning']='You already register, please log in'
          return errors  
        except:
          return errors
    
    def login_validator(self,postData):
      errors = {}
      try:
        user=User.objects.get(email_address=(postData['mail'].lower()))       
      except:
        errors['warning']='Invalid E-mail and password'
        return errors
      if not bcrypt.checkpw(postData['psd1'].encode(),user.password.encode()):
        errors['warning']='Invalid E-mail and password'
      
      return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password =models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    DOB=models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects=UserManager()