from django.shortcuts import render
from django.http import HttpResponse
from pints_main.models import Brewery, Beer, Beer_Score

def main_page(request):
	'''
	Queries database for a list of all beers/ breweries
	currently in DB. Retrieves 5 most recent of each and places
	in context dict
	'''
	brewery_list = Brewery.objects.order_by('-date_added')[:5]
	beer_list = Beer.objects.order_by('-date_added')[:5]
	context_dict = {'breweries': brewery_list, 'beers': beer_list}
	return render(request, 'pints_main/main_page.html', context_dict)
