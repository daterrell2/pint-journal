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

def beer_detail(request, beer_name_slug):
	context_dict = {}

	try:
		beer = Beer.objects.get(slug = beer_name_slug)
		context_dict['beer'] = beer
		context_dict['brewery'] = beer.brewery
		beer_score = beer.get_top_score()
		context_dict['beer_score'] = beer_score

	except beer.DoesNotExist:
		return redirect('/')

	return render(request, 'pints_main/beer_detail.html', context_dict)

def brewery_detail(request, brewery_name_slug):
	context_dict = {}

	try:
		brewery = Brewery.objects.get(slug = brewery_name_slug)
		context_dict['brewery'] = brewery
		beers = brewery.get_beers()
		context_dict['beers'] = beers

	except Brewery.DoesNotExist:
		return redirect('/')

	return render(request, 'pints_main/brewery_detail.html', context_dict)
