from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
#from utils.unique_slugify import unique_slugify
from django.contrib.auth.models import User
from utils import brewerydb

# class Brewery(models.Model):
# 	brewery_id = models.CharField(max_length=128, unique=True) #BreweryDB id
# 	date_added = models.DateTimeField(auto_now = True)
# 	date_modified = models.DateTimeField(auto_now_add = True)

# 	def __unicode__(self):
# 		return self.brewery_id

# class Beer(models.Model):
#	beer_id = models.CharField(max_length=128, unique=True) #BreweryDB id
#	brewery_id
# 	date_added = models.DateTimeField(auto_now = True)
# 	date_modified = models.DateTimeField(auto_now_add = True)

# 	def __unicode__(self):
# 		return self.beer_id

class BeerScore(models.Model):
	beer = models.CharField(max_length=128, blank=False) # id of beer in BreweryDB, called via API
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

	def get_beer(self, options={'withBreweries':'Y'}):
		'''
		API call to brewerydb where id == beer_score.beer
		Returns a tuple: beer_score and 'data' element from brewerydb dictionary
		(or beer_score, None)
		'''
		return brewerydb.BreweryDb.beer(self.beer, options).get('data')

class BeerScoreArchive(models.Model):
	'''
	stores user's score history for each beer.
	'''
	beer = models.CharField(max_length=128, blank=False)
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

	def get_beer(self, options={'withBreweries':'Y'}):
		'''
		API call to brewerydb where id == beer_score.beer
		Returns none or 'data' eleement from brewerydb dictionary
		'''
		return brewerydb.BreweryDb.beer(self.beer, options).get('data')