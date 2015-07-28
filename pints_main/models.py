from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Beer(models.Model):
    '''
    Holds data about beers pulled from BreweryDB via API
    '''
    # beer_id must be a valid beer id in BreweryDB API
    beer_id = models.CharField(max_length=128, blank=False, unique=True)

    def __unicode__(self):
        return str(self.beer_id)


class BeerScore(models.Model):
	beer = models.ForeignKey(Beer, blank=False, related_name='beerscores')
	user = models.ForeignKey(User, blank=False, related_name = 'beerscores')
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

	def save(self, *args, **kwargs):
		'''
		Automatically add old score to BeerScoreArchive
		if different from new score
		'''
		if self.pk:
			old_score = BeerScore.objects.get(pk=self.pk).score
			if self.score != old_score:
				archive = BeerScoreArchive(beer=self.beer, user=self.user, score=old_score)
				archive.save()

		super(BeerScore, self).save(*args, **kwargs)


class BeerScoreArchive(models.Model):
	'''
	stores user's score history for each beer.
	'''
	beer = models.ForeignKey(Beer, blank=False, related_name='beerscore_archives')
	user = models.ForeignKey(User, blank=False, related_name = 'beerscore_archives')
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