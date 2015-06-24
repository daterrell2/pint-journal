import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pint_journal_project.settings')

import django
django.setup()

from pints_main.models import Brewery, Beer, BeerScore
from django.contrib.auth.models import User

user = User.objects.get(username=u'david')

def populate():
	BeerScore.objects.all().delete()
	Beer.objects.all().delete()
	Brewery.objects.all().delete()

	brew_1 = add_brew('Souther Tier', 'United States', 'Micro', '',)
	brew_2 = add_brew('Port City', 'United States', 'Micro', '')
	brew_3 = add_brew('DC Brau', 'United States', 'Micro', '')

	beer_1 = add_beer(brewery=brew_1,
		name = 'Creme Brulee',
		beer_style = 'Milk Stout')

	beer_2 = add_beer(brewery=brew_1,
		name = '2x IPA',
		beer_style = 'American IPA')

	beer_3 = add_beer(brewery=brew_2,
		name = 'Porter',
		beer_style = 'American Porter')

	beer_4 = add_beer(brewery=brew_2,
		name = 'Optimal Wit',
		beer_style = 'Witbier')

	beer_5 = add_beer(brewery=brew_3,
		name='The Corruption',
		beer_style='American IPA')

	beer_6 = add_beer(brewery=brew_3,
		name='The Public Ale',
		beer_style='American Pale Ale')

	add_score(beer = beer_1, score = 95)

	add_score(beer = beer_2, score = 85)

	add_score(beer = beer_3, score = 80)

	add_score(beer = beer_4, score = 90)

	add_score(beer = beer_5, score = 85)

	add_score(beer = beer_6, score = 90)

def add_brew(name, country, brew_type, url):
	b = Brewery()
	b.name = name
	b.country = country
	b.brew_type = brew_type
	b.url = url
	b.save()
	return b

def add_beer(brewery, name, beer_style):
	br = Beer()
	br.brewery = brewery
	br.name = name
	br.beer_style = beer_style
	br.save()
	return br

def add_score(beer, score, user=user):
	s = BeerScore()
	s.beer = beer
	s.user = user
	s.score = score
	s.save()
	return s

if __name__ == '__main__':
	print "Starting db population script"
	populate()




