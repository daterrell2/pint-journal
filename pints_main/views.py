from django.shortcuts import render, redirect, HttpResponse
from pints_main.models import BeerScore, BeerScoreArchive, Beer
from pints_main.forms import BeerScoreForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from utils.brewerydb import BreweryDb, BreweryDbObject
from pints_user.model_utils import get_user
from utils.url_params import get_param
from django.db.models import Avg, Count
import re
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
	Generates sorted list of beers based on url querystring.
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

		if beer.beerscores.count() > 2:
			avg_score = int(round(beer.beerscores.aggregate(avg_score = Avg('score'))['avg_score']))
		else:
			avg_score = None

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

	If user has rated this beer, displays score and average score for all users.

	If user has not rated, displays form for new score that submits back to this view.

	Takes GET paramerter 'edit'. If '?edit=TRUE' (and user has already rated this beer)
		renders form with user's current score filled in as value.

		Submitting this form updates score in DB and adds old score to BeerScoreArchive.
	'''

	context_dict = {}

	user=get_user(request) # None or user object
	beer=Beer.objects.get_or_create(beer_id=beer_id)[0]

	context_dict['user'] = user
	context_dict['form_placeholder'] = 'score'
	context_dict['edit'] = False

	if request.method == 'POST':

		edit_flag=False

		try:
			new_score = BeerScore.objects.get(beer=beer, user=user)
			old_score_val = new_score.score
			edit_flag=True


		except BeerScore.DoesNotExist:
			new_score = BeerScore(beer=beer, user=user)

		form = BeerScoreForm(request.POST)

		if form.is_valid():
			form_score = form.save(commit=False)
			new_score.score = form_score.score

			if not edit_flag:
				new_score.save()
			else:
				new_score.save()
				if new_score.score != old_score_val:
					old_score = BeerScoreArchive(beer=beer, user=user, score=old_score_val)
					old_score.save()

			return redirect('/beer/' + beer_id)

		else:
			context_dict['form_placeholder'] = request.POST.get('score')
			print "INVALID!!!"
			print form.errors

	else:
		form = BeerScoreForm()

	context_dict['form'] = form

	# Beer Details
	beer_details = BreweryDb.beer(beer.beer_id, {'withBreweries':'Y'})

	if not beer_details or beer_details.get('status') != 'success':
		return redirect('index')

	context_dict['beer'] = beer
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
		return render(request, 'pints_main/beer_detail_user.html', context_dict)		

	return render(request, 'pints_main/beer_detail.html', context_dict)

@login_required
def add_score(request, beer_id):
	'''
	Handles AJAX request/ response for if
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



@login_required
def brewery_detail(request, brewery_id):

	context_dict = {}

	# get brewery detail
	brewery = BreweryDb.brewery(brewery_id)

	if brewery and brewery.get('status') == 'success':
		context_dict['brewery'] = BreweryDbObject(brewery)
	else:
		return redirect('index')

	# get user detail
	user=User.objects.get(id=request.user.id)
	context_dict['user'] = user

	# get any beers for brewery + each beer's score
	beers = BreweryDb.brewery_beers(brewery_id)

	if beers and beers.get('status') == 'success':

		for b in beers['data']:
			beer_id = b['id']
			all_scores = BeerScore.objects.filter(beer=beer_id)
			if all_scores:
			 	avg_score = all_scores.aggregate(Avg('score'))['score__avg']
			 	b['avg_score'] = int(round(avg_score))
			else:
				b['avg_score'] = None

			user_score = BeerScore.objects.filter(beer=beer_id, user=user)

			if user_score:
				b['user_score']  = user_score[0].score
			else:
				b['user_score'] = None

		context_dict['beers'] = BreweryDbObject(beers)

	else:
		context_dict['beers'] = None

	return render(request, 'pints_main/brewery_detail.html', context_dict)

@login_required
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

		results = BreweryDbObject(search_request)
		context_dict['results'] = results

		last_page = int(results.numberOfPages)
		if last_page > 1:

			if p >= num_pages:
				pages = range(p, min(last_page, p + num_pages) +1)

			else:
				pages = range(1, num_pages+1)

	context_dict['pages'] = pages

	return render(request, 'pints_main/search_results.html', context_dict)








# @login_required
# def add_brewery(request):
# 	if request.method=='POST':
# 		form = BreweryForm(request.POST)

# 		if form.is_valid():
# 			new_brewery = form.save(commit=True)
# 			return redirect('/brewery/'+new_brewery.slug)

# 		else:
# 			print form.errors

# 	else:
# 		form = BreweryForm()

# 	return render(request, 'pints_main/add_brewery.html', {'form':form})

# @login_required
# def add_beer(request, brewery_name_slug):

#  	try:
# 		brewery = Brewery.objects.get(slug=brewery_name_slug)

# 	except Brewery.DoesNotExist:
# 		brewery = None

# 	if request.method=='POST':
# 		form = BeerForm(request.POST)

# 		if form.is_valid():
# 			if brewery:
# 				beer = form.save(commit=False)
# 				beer.brewery = brewery
# 				beer.save()

# 				return redirect('/beer/'+beer.slug)

# 		else:
# 			print form.errors

# 	else:
# 		form = BeerForm()

# 	context_dict={'form':form, 'brewery':brewery}

# 	return render(request, 'pints_main/add_beer.html', context_dict)

# @login_required
# def edit_beer(request, beer_name_slug):

# 	try:
# 		beer = Beer.objects.get(slug=beer_name_slug)

# 	except Beer.DoesNotExist:
# 		redirect('index')

# 	if request.method=='POST':
# 		form = BeerForm(request.POST, instance = beer)

# 		if form.is_valid():
# 				beer = form.save(commit=False)
# 				beer.save()
# 				return redirect(beer.get_absolute_url())

# 		else:
# 			print form.errors

# 	else:
# 		form = BeerForm(instance = beer)

# 	context_dict={'form':form, 'beer':beer}

# 	return render(request, 'pints_main/edit_beer.html', context_dict)

# @login_required
# def delete_beer(request, beer_name_slug):

# 	try:
# 		beer = Beer.objects.get(slug=beer_name_slug)
# 		brewery = beer.brewery

# 	except:
# 		redirect('index')

# 	if request.method=='POST':
# 		beer.delete()
# 		return redirect(brewery.get_absolute_url())
# 	else:
# 		return render(request, 'pints_main/delete_beer.html', {'beer':beer})