import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pint_journal_project.settings')

import django
django.setup()

from pints_main.models import BeerScore
from pints_main.utils.brewerydb import *
from django.contrib.auth.models import User

user = User.objects.get(username=u'david')

def populate():

	beers = ['zGBmz4', 'kZsjqY', '9KiCpK', 'Kax7jD', 'nEEnk1', 'kckAgC']
	BeerScore.objects.all().delete()
	for i in range(len(beers)):
		add_score(beers[i], 80+i)


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




