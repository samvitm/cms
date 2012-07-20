from django.contrib.auth.models import User
from django.db import models

# Create your models here.

PAYMENT_CHOICES=(
  ('cc','Credit Card'),
  ('dc','Debit Card'),
)

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

class Package(models.Model):
 includes = models.CharField(max_length=200)
 amount = models.IntegerField()
 conference = models.ForeignKey(Conference)

 def __unicode__(self):
   return str(self.conference)+' - Rs'+str(self.amount)+' : '+str(self.includes)


class Payment(models.Model):
  conference = models.ForeignKey(Conference)
  payment_from = models.ForeignKey(User)
  mode = models.CharField(choices=PAYMENT_CHOICES,max_length=100)
  cardno = models.CharField(max_length=100)
  package = models.ForeignKey(Package)
  transaction_id = models.CharField(max_length=20)
  verified = models.BooleanField()
  time = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return str(self.payment_from)+'-' + str(self.conference)


class Area(models.Model):
  area_no = models.CharField(max_length=100,verbose_name='Area name ')

  def __unicode__(self):
    return str(self.area_no)

class Banner(models.Model):
  name = models.CharField(max_length=100,verbose_name='Name of sponsor')
  area = models.ForeignKey(Area)
  author = models.ForeignKey(User)
  image = models.FileField(upload_to='sponsor_banners/',verbose_name='Sponsor logo image ')

  def __unicode__(self):
    return  self.name