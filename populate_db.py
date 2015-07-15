import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pint_journal_project.settings')

import django
django.setup()

from pints_main.models import BeerScore, Beer
from pints_main.utils.brewerydb import *
from django.contrib.auth.models import User

users = [User.objects.get(username=u) for u in [u'david', u'david_test', u'new']]

def populate():

	beer_ids = ['zGBmz4', 'kZsjqY', '9KiCpK', 'Kax7jD', 'nEEnk1', 'kckAgC']
	BeerScore.objects.all().delete()
	Beer.objects.all().delete()

	beers = [add_beer(i) for i in beer_ids]

	for i in range(len(beers)):
		for n in range(len(users)):
			add_score(beers[i], 80+i+n, users[n])

def add_beer(beer_id):
	b = Beer(beer_id = beer_id)
	b.save()
	return b


def add_score(beer, score, user):
	s = BeerScore()
	s.beer = beer
	s.user = user
	s.score = score
	s.save()
	return s

if __name__ == '__main__':
	print "Starting db population script"
	populate()




