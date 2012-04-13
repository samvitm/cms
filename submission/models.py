from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Submission(models.Model):
  title = models.CharField(max_length=100)
  abstract = models.TextField()
  status = models.NullBooleanField()
  authors = models.ManyToManyField(User,related_name='authors')
  topic = models.ManyToManyField('TopicArea')
  comments = models.ManyToManyField('Comments')
  reviewers = models.ManyToManyField(User,related_name='reviewers')
  paper = models.FileField(upload_to='/paper_uploads')

class TopicArea(models.Model):
  topic = models.CharField(max_length=100)

class Comments(models.Model):
  comment = models.TextField()
  author = models.ForeignKey(User)