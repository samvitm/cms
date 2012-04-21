from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from cms.conference.models import Conference

class Submission(models.Model):
  title = models.CharField(max_length=100)
  abstract = models.TextField()
  status = models.NullBooleanField()
  author = models.ForeignKey(User)
  topic = models.ManyToManyField('TopicArea',help_text='To help match submissions to reviewers and sessions, please select one or more area(s) most applicable to your submission')
  reviewers = models.ManyToManyField(User,related_name='reviewers')
  paper = models.FileField(upload_to='paper_uploads')
  conference = models.ForeignKey(Conference)



  def __unicode__(self):
    return self.title

class TopicArea(models.Model):
  topic = models.CharField(max_length=100)

  def __unicode__(self):
    return str(self.topic)

class Comments(models.Model):
  comment = models.TextField()
  author = models.ForeignKey(User)
  time = models.DateTimeField(auto_now_add=True)
  submission = models.ForeignKey(Submission,related_name='sub')

  class Meta:
    verbose_name_plural = 'Comments'
    verbose_name = 'Comment'

class Author(models.Model):
  first_name = models.CharField(max_length=100)
  last_name  = models.CharField(max_length=100)
  organisation = models.CharField(max_length=100)
  country = models.CharField(max_length=100)
  email = models.EmailField()
  submission = models.ForeignKey(Submission,related_name='submission')