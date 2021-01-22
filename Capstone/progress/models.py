from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
  pass

class Started(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=2)
  started = models.CharField(max_length=140)
  modifiedDate = models.DateTimeField(default=timezone.now)
  stfnew_value = models.BooleanField(null=True)
  def serialize(self, user):
    return {
      "started":self.started,
      "modifiedDate": self.modifiedDate,
      "modifiedUser": self.user.username,
      "stfnew_value": self.stfnew_value,
    }

  # def __str__(self):
  #   return {
  #     f'Started Task: {self.started}'
  #   }

class Proceeding(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  proceeding = models.CharField(max_length=140)
  modifiedDate = models.DateTimeField(default=timezone.now)
  ptfnew_value = models.BooleanField(null=True)
  
  def serialize(self, user):
    return {
      "proceeding":self.proceeding,
      "modifiedDate": self.modifiedDate,
      "modifiedUser": self.user.username,
      "ptfnew_value": self.ptfnew_value,

    }
  
  # def __str__(self):
  #   return {
  #     f'Proceeding Task: {self.proceeding}'
  #   }

class Completed(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  completed = models.CharField(max_length=140)
  modifiedDate = models.DateTimeField(default=timezone.now)
  cotfnew_value = models.BooleanField(null=True)


  def serialize(self, user):
    return {
      "completed":self.completed,
      "modifiedDate": self.modifiedDate,
      "modifiedUser": self.user.username,
      "cotfnew_value": self.cotfnew_value,

    }

  # def __str__(self):
  #   return {
  #     f'Completed Task: {self.completed}'
  #     }


class Cancelled(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  cancelled = models.CharField(max_length=140)
  modifiedDate = models.DateTimeField(default=timezone.now)
  catfnew_value = models.BooleanField(null=True)

  
  def serialize(self, user):
    return {
      "cancelled":self.cancelled,
      "modifiedDate": self.modifiedDate,
      "modifiedUser": self.user.username,
      "catfnew_value": self.catfnew_value,

    }

  # def __str__(self):
  #   return {
  #     f'Cancelled Task: {self.cancelled}'
  #     }


