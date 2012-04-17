from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Program(models.Model):
  name = models.CharField(max_length=100)
  venue = models.CharField(max_length=100)
  start_date_time = models.DateTimeField()
  end_date_time = models.DateTimeField()
  conference = models.ForeignKey('Conference')

  def __unicode__(self):
    return str(self.conference) + '-' + str(self.name)

class Conference(models.Model):
  name = models.CharField(max_length=100)
  about = models.TextField()
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  venue = models.CharField(max_length=190)
  admin = models.ForeignKey(User)

  def __unicode__(self):
    return str(self.name)

class Lecture(models.Model):
  program = models.ForeignKey(Program)
  name = models.CharField(max_length=100)
  description = models.TextField()