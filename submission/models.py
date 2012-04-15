from django.contrib.auth.models import User
from django.db import models

# Create your models here.
#TODO Create models for Author to add in a submission
class Submission(models.Model):
  title = models.CharField(max_length=100)
  abstract = models.TextField()
  status = models.NullBooleanField()
  #TODO - Change to foreign key
  authors = models.ManyToManyField(User,related_name='authors')
  topic = models.ManyToManyField('TopicArea',help_text='To help match submissions to reviewers and sessions, please select one or more area(s) most applicable to your submission')
  comments = models.ManyToManyField('Comments',)
  reviewers = models.ManyToManyField(User,related_name='reviewers')
  paper = models.FileField(upload_to='paper_uploads')


  def __unicode__(self):
    return self.title

class TopicArea(models.Model):
  topic = models.CharField(max_length=100)

  def __unicode__(self):
    return str(self.topic)

class Comments(models.Model):
  comment = models.TextField()
  author = models.ForeignKey(User)

  class Meta:
    verbose_name_plural = 'Comments'