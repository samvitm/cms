from django.db import models
from django.contrib.auth.models import User

USER_TYPES = (
  ('Author','Author'),
  ('Delegate','Delegate'),
  ('ConfAdmin','Conference Administrator'),
  ('Reviewer','Reviewer'),
  ('Sponsor','Sponsor'),
)


class UserProfile(models.Model):
  address = models.TextField(max_length=200)
  phone_number = models.CharField(max_length=20)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  country = models.CharField(max_length=100)
  type = models.CharField(max_length=100,choices=USER_TYPES)
  user = models.ForeignKey(User, unique=True)

  def __unicode__(self):
    return str(self.user.username)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])