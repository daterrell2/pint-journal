from django.db import models
from django.template.defaultfilters import slugify

class Brewery(models.Model):
	name = models.CharField(max_length=128, unique=True)
	country = models.CharField(max_length=128)
	url = models.URLField()
	slug = models.SlugField(unique = True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Brewery, self).save(*args, **kwargs)

class Beer(models.Model):
	brewery = models.ForeignKey(Brewery)
	name = models.CharField(max_length=128)
	style = models.CharField(max_length=128)
	slug = models.SlugField(unique = True)

	class Meta:
		unique_together = ('brewery', 'name')

	def save(self, *args, **kwargs):
		unique_name = '-'.join(self.brewery, self.name)
		self.slug = slugify(unique_name)
		super(Beer, self).save(*args, **kwargs)

class Score(models.Model):
	beer = models.ForeignKey(Beer)
	score = models.IntegerField()
	score_date = models.DateTimeField(auto_now = True)
	#user = models.ForeignKey('django.contrib.auth.models.User')


