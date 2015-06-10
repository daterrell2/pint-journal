from django.db import models
from django.template.defaultfilters import slugify

class Brewery(models.Model):
	name = models.CharField(max_length=128, unique=True)
	country = models.CharField(max_length=128)
	brew_type = models.CharField(max_length=128, blank=True)#change to foreign key lookup
	url = models.URLField()
	slug = models.SlugField(unique = True)
	date_added = models.DateTimeField(auto_now = True)
	date_modified = models.DateTimeField(auto_now_add = True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Brewery, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

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
		unique_name = '-'.join([self.brewery.name, self.name])
		self.slug = slugify(unique_name)
		super(Beer, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class Beer_Score(models.Model):
	beer = models.ForeignKey(Beer)
	score = models.IntegerField()
	score_date = models.DateTimeField(auto_now = True)	
	#user = models.ForeignKey('django.contrib.auth.models.User')

#class Beer_Style_Lookup(models.Model):

#class Brew_Type_Lookup(models.Mode):