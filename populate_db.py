import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pint_journal_project.settings')

import django
django.setup()

from pints_main.models import BeerScore, Beer
#from pints_main.utils.brewerydb import *
from django.contrib.auth.models import User
import random
from pints_main.utils.random_string import random_string

def populate():

    users = [add_user('tmp_user' + str(i)) for i in range(10)]

    beer_ids = ['zGBmz4', 'kZsjqY', '9KiCpK', 'Kax7jD', 'nEEnk1', 'kckAgC']

    beers = [add_beer(i) for i in beer_ids]

    for b in beers:
		for u in users:
			add_score(b, random.randint(0,100), u)

def add_beer(beer_id):
	b, created = Beer.objects.get_or_create(beer_id = beer_id)
	return b


def add_score(beer, score, user):
	s, created = BeerScore.objects.get_or_create(beer=beer, user=user)
	s.score = score
	s.save()
	return s

def add_user(username):
    u, created = User.objects.get_or_create(username = username)
    if created:
        u.set_password(random_string())
        u.save()
    return u

if __name__ == '__main__':
	print "Starting db population script"
	populate()




