from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from utils import brewerydb

class Beer(models.Model):
	beer_id = models.CharField(max_length=128, blank=False, unique=True)

	def __unicode__(self):
		return str(self.beer_id)

	def get_avg_score(self):
		'''
		returns average beerscore for beer
		'''
		scores = BeerScore.objects.filter(beer=self)
		avg_score = scores.aggregate(models.Avg('score'))['score__avg']
		return int(round(avg_score))


class BeerScore(models.Model):
	beer = models.ForeignKey(Beer, blank=False)
	user = models.ForeignKey(User, blank=False)
	score = models.IntegerField(
		default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
            ]
        )
	score_date = models.DateTimeField(auto_now = True)

	class Meta:
		unique_together = ('beer', 'user')

	def __unicode__(self):
		return str(self.score)

class BeerScoreArchive(models.Model):
	'''
	stores user's score history for each beer.
	'''
	beer = models.ForeignKey(Beer, blank=False)
	user = models.ForeignKey(User, blank=False)
	score = models.IntegerField(
		default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
            ]
        )
	score_date = models.DateTimeField(auto_now = True)	

	def __unicode__(self):
		return str(self.score)