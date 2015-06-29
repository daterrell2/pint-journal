from django.db import models
from unidecode import unidecode
from utils.unique_slugify import unique_slugify

class Brewery(models.Model):
	name = models.CharField(max_length=128, unique=True)
	country = models.CharField(max_length=128)
	brew_type = models.CharField(max_length=128, blank=True)#change to foreign key lookup
	url = models.URLField()
	slug = models.SlugField(unique = True)
	date_added = models.DateTimeField(auto_now = True)
	date_modified = models.DateTimeField(auto_now_add = True)

	def save(self, *args, **kwargs):
		unique_slugify(self, unidecode(self.name))
		super(Brewery, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

	def get_beers(self):
		return Beer.objects.filter(brewery = self).order_by('-date_added')

	def get_absolute_url(self):
		return '/brewery/%s' % self.slug

class Beer(models.Model):
	brewery = models.ForeignKey(Brewery)
	name = models.CharField(max_length=128)
	beer_style = models.CharField(max_length=128)#change to foreign key lookup
	slug = models.SlugField(unique = True)
	date_added = models.DateTimeField(auto_now = True)
	date_modified = models.DateTimeField(auto_now_add = True)

	class Meta:
		unique_together = ('brewery', 'name')

	def save(self, *args, **kwargs):
		unique_name = '%s-%s' %(self.brewery.name, self.name)
		unique_slugify(self, unique_name)
		#self.slug = urllib.quote(unique_name)
		super(Beer, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

	def get_top_score(self):
		try:
			top_score = BeerScore.objects.filter(beer = self).order_by('-score_date')[0]
			return top_score

		except IndexError:
			return None

	def get_absolute_url(self):
		return '/beer/%s' % self.slug

class BeerScore(models.Model):
	beer = models.ForeignKey(Beer)
	score = models.IntegerField()
	score_date = models.DateTimeField(auto_now = True)	
	#user = models.ForeignKey('django.contrib.auth.models.User')

	def __unicode__(self):
		return str(self.score)


#class Beer_Style_Lookup(models.Model):

#class Brew_Type_Lookup(models.Mode):





