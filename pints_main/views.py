from django.shortcuts import render, redirect
from django.http import HttpResponse
from pints_main.models import BeerScore
from pints_main.forms import BeerScoreForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from utils.brewerydb import BreweryDb
from django.db.models import Avg
import re

@login_required
def index(request):
	'''
	Looks for query string in url '?view=beer' or '?view=brewery' and renders
	index.html with appropriate object. Default view is 'beer'
	'''

	if not request.user.is_authenticated:
		user = None

	else:
		try:
			user=User.objects.get(id=request.user.id)
		except User.DoesNotExist:
			user = None

	scores = []
	sort_choices = ['^-?score_date$', '^-?score$']
	sort_pattern = '|'.join(sort_choices)
	default_sort = '-score_date'

	# get url params
	sort_param = request.GET.get('sort')
	view_param = request.GET.get('view')

	if sort_param and re.match(sort_pattern, sort_param):
		sort = sort_param
	else:
		sort = default_sort

	if user and view_param != 'all':
		scores = BeerScore.objects.filter(user=user)
		if scores:
			scores = scores.order_by(sort)[:6]

	else:
		scores = BeerScore.objects.order_by(sort)[:6]

	scores_detail = []
	for score in scores:
		beers = score.get_beer()
		if beers:
			name = beers.get('name')
			style = beers['style']['category']['name']
			brewery = beers.get('breweries')
			icon = brewery[0]['images']['medium']

		else:
			name, style, icon = None, None, None
		
		scores_detail.append({'name':name, 'style':style, 'score':score.score, 'id':score.id, 'icon':icon, 'beer_id':score.beer})

	context_dict = {'scores_detail': scores_detail}
	return render(request, 'pints_main/index.html', context_dict)

@login_required
def beer_detail(request, beer_id):

	fields = ['user', 'beer_score', 'beer_name', 'beer_style', 'beer_desc', 'breweries', 'brewery_img', 'brewery_id']
	context_dict = {f:'' for f in fields}

	# User score
	user=User.objects.get(id=request.user.id)
	context_dict['user'] = user

	beer_score = BeerScore.objects.filter(beer = beer_id, user = user)
	if beer_score:
		context_dict['beer_score'] = beer_score[0]

	beer = BreweryDb.beer(beer_id, {'withBreweries':'Y'}).get('data')

	if not beer:
		return redirect('index')

	# Beer details
	context_dict['beer_name'] = beer['name']
	context_dict['beer_style'] = beer['style']['category']['name']
	context_dict['beer_desc'] = beer['description']
	
	breweries = beer.get('breweries')
	if breweries:
		context_dict['breweries'] = breweries
		brewery = breweries[0] #pick first brewery listed
		context_dict['brewery_img'] = brewery['images']['medium']
		context_dict['brewery_id'] = brewery['id']

	# Average score
	all_scores = BeerScore.objects.filter(beer=beer_id)
	if all_scores:
		 avg_score = all_scores.aggregate(Avg('score'))['score__avg']
		 context_dict['avg_score'] = int(round(avg_score))
	else:
		context_dict['avg_score'] = 'N/A'

	return render(request, 'pints_main/beer_detail.html', context_dict)

@login_required
def brewery_detail(request, brewery_id):

	fields = ['user', 'brewery_name', 'brewery_desc', 'brewery_url', 'brewery_img', 'beers']
	context_dict = {f:'' for f in fields}

	user=User.objects.get(id=request.user.id)
	context_dict['user'] = user

	brewery = BreweryDb.brewery(brewery_id).get('data')

	if not brewery:
		return redirect('index')

	context_dict['brewery_name'] = brewery['name']
	context_dict['brewery_desc'] = brewery['description']
	context_dict['brewery_url'] = brewery['website']
	context_dict['brewery_img'] = brewery['images']['large']

	beers = BreweryDb.brewery_beers(brewery_id).get('data')

	for b in beers:
		beer_id = b['id']
		all_scores = BeerScore.objects.filter(beer=beer_id)
		if all_scores:
		 	avg_score = all_scores.aggregate(Avg('score'))['score__avg']
		 	b['avg_score'] = int(round(avg_score))
		else:
			b['avg_score'] = 'N/A'

		user_score = BeerScore.objects.filter(beer=beer_id, user=user)

		if user_score:
			b['user_score']  = user_score[0].score

	context_dict['beers'] = beers

	return render(request, 'pints_main/brewery_detail.html', context_dict)

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