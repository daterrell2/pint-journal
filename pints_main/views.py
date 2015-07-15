from django.shortcuts import render, redirect
from pints_main.models import BeerScore, BeerScoreArchive, Beer
from pints_main.forms import BeerScoreForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from utils.brewerydb import BreweryDb, BreweryDbObject
from pints_user.model_utils import get_user
from model_utils import get_sorted_avg
from utils.url_params import get_param
from django.db.models import Avg
import re

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
	Looks for query string in url '?view=beer' or '?view=brewery' and renders
	index.html with appropriate object. Default view is 'beer'
	'''

	user = get_user(request) # None or User object

	sort_choices = ['score', '-score']
	display_choices = ['grid', 'list']

	# get url params
	sort_param = get_param(request=request, param='sort', options=sort_choices, default=sort_choices[0])
	display_param = get_param(request=request, param='display', options=display_choices)

	sort_reverse = True
	if sort_param[0] == '-':
		sort_reverse = False

	beers = get_sorted_avg(sort_reverse=sort_reverse, limit=12)
	beer_list = []
	for b in beers:
		beer = BreweryDb.beer(b.beer_id, {'withBreweries':'Y'})
		if beer and beer.get('status') == 'success':
			beer['data']['score'] = int(round(b.score))
			beer_list.append(beer)

	context_dict = {'beer_list': beer_list, 'user' : user}
	return render(request, 'pints_main/index_grid.html', context_dict)

@login_required
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

	user=User.objects.get(id=request.user.id)

	context_dict['user'] = user
	context_dict['form_placeholder'] = 'score'
	context_dict['edit'] = False

	if request.method == 'POST':

		edit_flag=False

		try:
			new_score = BeerScore.objects.get(beer=beer_id, user=user)
			old_score_val = new_score.score
			edit_flag=True


		except BeerScore.DoesNotExist:
			new_score = BeerScore(beer=beer_id, user=user)

		form = BeerScoreForm(request.POST)

		if form.is_valid():
			form_score = form.save(commit=False)
			new_score.score = form_score.score

			if not edit_flag:
				new_score.user = user
				new_score.beer = beer_id
				new_score.save()
			else:
				new_score.save()
				if new_score.score != old_score_val:
					old_score = BeerScoreArchive(beer=beer_id, user=user, score=old_score_val)
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
	beer = BreweryDb.beer(beer_id, {'withBreweries':'Y'})

	if not beer or beer.get('status') != 'success':
		return redirect('index')

	context_dict['beer'] = BreweryDbObject(beer)

	# User score
	beer_score = BeerScore.objects.filter(beer = beer_id, user = user)
	if beer_score:
		context_dict['beer_score'] = beer_score[0]
		context_dict['form_placeholder'] = beer_score[0].score
		if request.GET.get('edit') == 'True':
			context_dict['edit'] = True

	# Average score
	all_scores = BeerScore.objects.filter(beer=beer_id)
	if all_scores:
		 avg_score = all_scores.aggregate(Avg('score'))['score__avg']
		 context_dict['avg_score'] = int(round(avg_score))
	else:
		context_dict['avg_score'] = None

	return render(request, 'pints_main/beer_detail.html', context_dict)

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