from django.shortcuts import render, redirect, HttpResponse
from pints_main.models import BeerScore, Beer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from utils.brewerydb import BreweryDb, BreweryDbObject
from pints_user.model_utils import get_user
from utils.url_params import get_param
from django.db.models import Avg, Count
import json

def welcome(request):
    '''
    Redirects logged in users to homepage.
    Otherwises renders cover page
    '''
    if request.user.is_authenticated():
		return redirect('index')

    return render(request, 'pints_main/welcome.html')

def index(request):
	'''
	Generates sorted list of beers based on url query string.
	Renders beer list either to grid template (index_grid.html)
		or list template(index_list.html)
	'''

	user = get_user(request) # None or User object

	sort_choices = ['-score', 'score']
	display_choices = ['grid', 'list']
	view_choices = ['user', 'all']

	# get url params
	sort_param = get_param(request, 'sort', sort_choices, default='-score')
	display_param = get_param(request, 'display', display_choices, default='grid')
	view_param = get_param(request, 'view', view_choices, default='user')

	if user and view_param == 'user':
		scores = user.beerscores.all().order_by(sort_param)
		beers = [b.beer for b in scores]

	else:
		view_param = 'all'
		beer_count = Beer.objects.annotate(num_scores=Count('beerscores')).filter(num_scores__gte=2) # only average beers with more than one score
		beers = beer_count.annotate(score = Avg('beerscores__score')).order_by(sort_param)

	beer_list = []

	for beer in beers:
		try:
			user_score = beer.beerscores.get(user=user)

		except BeerScore.DoesNotExist:
			user_score = None

		if beer.beerscores.count() >= 2:
			avg_score = int(round(beer.beerscores.aggregate(avg_score = Avg('score'))['avg_score']))
		else:
			avg_score = None

		# API call to BreweryDb
		b = BreweryDb.beer(beer.beer_id, {'withBreweries':'Y'})
		if b and b.get('status') == 'success':
			b['data']['user_score'] = user_score
			b['data']['avg_score'] = avg_score
			beer_list.append(b)

	context_dict = {'beer_list': beer_list, 'user' : user, 'view':view_param, 'display':display_param, 'sort':sort_param}
	return render(request, 'pints_main/index_grid.html', context_dict)

def beer_detail(request, beer_id):
	'''
	Renders page for a single beer.

	If user is logged in, pulls in beer score/ button to add or edit score
		via AJAX requests to get_score() and get_form().

	User score POST requests are handled via AJAX post to add_score()

	If no user, only displays average score.
	'''

	context_dict = {}

	user=get_user(request) # None or user object
	beer=Beer.objects.get_or_create(beer_id=beer_id)[0]

	context_dict['user'] = user
	context_dict['beer'] = beer

	beer_details = BreweryDb.beer(beer.beer_id, {'withBreweries':'Y'})

	if not beer_details or beer_details.get('status') != 'success':
		return redirect('index')

	context_dict['beer_details'] = beer_details

	try:
		score = BeerScore.objects.get(beer=beer, user=user)
		context_dict['form_placeholder'] = score
		context_dict['beer_score'] = score

	except BeerScore.DoesNotExist:
		context_dict['beer_score'] = None

	if beer.beerscores.count() > 1:
		context_dict['avg_score'] = int(round(beer.beerscores.aggregate(a = Avg('score'))['a']))

	if request.GET.get('edit') == 'True':
			context_dict['edit'] = True

	if user:
		return render(request, 'pints_main/beer_detail/beer_detail_user.html', context_dict)

	return render(request, 'pints_main/beer_detail.html', context_dict)


# change to post only
@login_required
def get_form(request, beer_id):
	'''
	returns html form snippet for AJAX request from beer_detail_user
	'''
	user = get_user(request)

	try:
		beer=Beer.objects.get(beer_id=beer_id)
	except Beer.DoesNotExist:
		beer=None

	try:
		beer_score = BeerScore.objects.get(beer=beer, user=user)
	except BeerScore.DoesNotExist:
		beer_score = None

	return render(request, 'pints_main/beer_detail/beer_score_form.html', {'beer':beer, 'beer_score':beer_score})

# change to post only
@login_required
def get_score(request, beer_id):
	'''
	returns html snippet with beer score as <p> element
	for AJAX request from beer_detail_user
	'''

	user = get_user(request)
	try:
		beer = Beer.objects.get(beer_id = beer_id)
	except Beer.DoesNotExist:
		beer=None

	if beer:
		try:
			beer_score = BeerScore.objects.get(beer=beer, user=user)
		except BeerScore.DoesNotExist:
			beer_score=None
	else:
		beer_score = None

	return render(request, 'pints_main/beer_detail/beer_score.html', {'beer':beer, 'beer_score':beer_score})

@login_required
def add_score(request, beer_id):
	'''
	Handles AJAX request/ response for scores
	'''

	if request.method == 'POST':

		print "POST!!"

		user=User.objects.get(id=request.user.id)
		beer=Beer.objects.get_or_create(beer_id=beer_id)[0]

		response_data = {}

		score_val = request.POST.get('the_post')

		try:
			score_val = int(score_val)
			if score_val in range(101):
				score = BeerScore.objects.get_or_create(beer=beer, user=user)[0]
				score.score = score_val
				score.save()

				response_data['result'] = 'Success!'
				response_data['score'] = str(score_val)
				response_data['score_url'] = "/beer/"+beer_id+"/get_score"

			else:
				response_data['result'] = 'error1'
				response_data['error'] = 'Invalid score'


		except TypeError:
			response_data['result'] = 'error2'
			response_data['error'] = 'Invalid score'

		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
			)
	else:
		return HttpResponse(
			json.dumps({"nothing to see": "this isn't happening"}),
			content_type="application/json"
			)



def brewery_detail(request, brewery_id):

	context_dict = {}

	# get brewery detail
	brewery = BreweryDb.brewery(brewery_id)

	if brewery and brewery.get('status') == 'success':
		context_dict['brewery'] = BreweryDbObject(brewery)
	else:
		return redirect('index')

	# get user detail
	user=get_user(request)
	context_dict['user'] = user

	# get any beers for brewery + each beer's score
	beers = BreweryDb.brewery_beers(brewery_id)

	if beers and beers.get('status') == 'success':

		for b in beers['data']:
			beer= Beer.objects.get_or_create(beer_id = b['id'])[0]
			if beer.beerscores.count() > 1:
			 	avg_score = beer.beerscores.aggregate(a = Avg('score'))['a']
			 	b['avg_score'] = int(round(avg_score))
			else:
				b['avg_score'] = None

			user_score = BeerScore.objects.filter(beer=beer, user=user)

			if user_score:
				b['user_score']  = user_score[0].score
			else:
				b['user_score'] = None

		context_dict['beers'] = BreweryDbObject(beers)

	else:
		context_dict['beers'] = None

	return render(request, 'pints_main/brewery_detail.html', context_dict)


def search(request):
	context_dict = {}

	search_types=['beer', 'brewery']
	search_params=['q', 'type', 'p']

	pages = []
	num_pages = 10

	search_dict = {k: request.GET.get(k) for k in search_params}

	if search_dict['type'] not in search_types:
		search_dict['type'] = search_types[0]
	try:
		search_dict['p'] = int(search_dict['p'])
	except TypeError:
		search_dict['p'] = 1

	context_dict = search_dict

	if search_dict['type'] == 'beer':
		search_dict['withBreweries'] = 'Y'

	search_request = BreweryDb.search(search_dict)

	if search_request and search_request.get('status') == 'success':
		# current page
		p = context_dict['p']

		#results = BreweryDbObject(search_request)
		context_dict['results'] = search_request.get('data')

        try:
            last_page = int(search_request.get('numberOfPages'))

        except TypeError:
            last_page = 1

        if last_page > 1:

			if p >= num_pages:
				pages = range(p, min(last_page, p + num_pages) +1)

			else:
				pages = range(1, num_pages+1)

	context_dict['pages'] = pages

	return render(request, 'pints_main/search_results.html', context_dict)