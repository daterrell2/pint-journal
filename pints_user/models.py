from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    '''
    Extension of django's built in user model (one-to-one relation)
    '''
    user = models.OneToOneField(User)

    # custom user profile fields below
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username
