from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from submission.models import Submission,Comments

RATING_CHOICES = (
  ('Very Good','Very Good'),
  ('Good','Good'),
  ('Average','Average'),
  ('Poor','Poor'),
)

BID_CHOICES = (
  ('High','High - Very interested'),
  ('Medium','Interested'),
  ('Low','Not Interested'),
)
class Review(models.Model):
  reviewer = models.ForeignKey(User)
  submission = models.ForeignKey(Submission)
  recomendation = models.ForeignKey('Recomendation')
  overall_rating = models.CharField(max_length=100,choices=RATING_CHOICES)
  completed = models.BooleanField(verbose_name='I have completed the review')
  comments = models.ManyToManyField(Comments)

  def __unicode__(self):
    return 'Review of '+ str(self.submission)

class ReviewUpload(models.Model):
  review = models.ForeignKey(Review)
  file = models.FileField(upload_to='reviews')

  def __unicode__(self):
    return str(self.review)

class Bid(models.Model):
  submission = models.ForeignKey(Submission)
  bid = models.CharField(max_length=100,choices=BID_CHOICES)

class Recomendation(models.Model):
  recomendation = models.CharField(max_length=300)

  def __unicode__(self):
    return self.recomendation
