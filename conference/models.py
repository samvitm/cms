from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Program(models.Model):
  name = models.CharField(max_length=100)
  venue = models.CharField(max_length=100)
  start_date_time = models.DateTimeField()
  end_date_time = models.DateTimeField()


class Conference(models.Model):
  name = models.CharField(max_length=100)
  programs = models.ManyToManyField(Program)
  about = models.TextField()
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  venue = models.CharField(max_length=190)
  admin = models.ForeignKey(User)

class Lecture(models.Model):
  program = models.ForeignKey(Program)
  name = models.CharField(max_length=100)
  description = models.TextField()