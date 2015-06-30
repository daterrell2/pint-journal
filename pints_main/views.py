from django.shortcuts import render, redirect
from pints_main.models import BeerScore
from pints_main.forms import BeerScoreForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import re

def index(request):
	'''
	Looks for query string in url '?view=beer' or '?view=brewery' and renders
	index.html with appropriate object. Default view is 'beer'
	'''

	if request.user.is_authenticated:
		user=User.objects.get(id=request.user.id)

	scores = []
	user = None
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
			style = beers['style']['category'].get('name')
			brewery = beers.get('breweries')
			icon = brewery[0]['images']['icon']

		else:
			name, style, icon = None, None, None
		
		scores_detail.append({'name':name, 'style':style, 'score':score.score, 'id':score.id, 'icon':icon})
		
	context_dict = {'scores_detail': scores_detail}
	return render(request, 'pints_main/index.html', context_dict)

# def beer_detail(request, beer_score_id):
# 	'''
# 	Renders users score for a given beer, along with details from BreweryDB
# 	'''
# 	context_dict = {}

# 	try:
# 		beer_score = BeerScore.objects.get(id = beer_score_id)
# 		context_dict['beer_score'] = beer_score
# 		context_dict['beer'] = beer.brewery
# 		beer_score = beer.get_top_score()
# 		context_dict['beer_score'] = beer_score

# 	except beer.DoesNotExist:
# 		return redirect('/')

# 	if request.method=='POST':
# 		form = BeerScoreForm(request.POST)

# 		if form.is_valid():
# 			if beer:
# 				score = form.save(commit=False)
# 				score.beer=beer
# 				score.save()

# 				form = BeerScoreForm() #new blank form

# 				return redirect('/beer/'+beer.slug)

# 		else:
# 			print form.errors

# 	else:
# 		form = BeerScoreForm()

# 	context_dict['form'] = form
# 	return render(request, 'pints_main/beer_detail.html', context_dict)

# def brewery_detail(request, brewery_name_slug):
# 	context_dict = {}

# 	try:
# 		brewery = Brewery.objects.get(slug = brewery_name_slug)
# 		context_dict['brewery'] = brewery
# 		beers = brewery.get_beers()
# 		context_dict['beers'] = beers

# 	except Brewery.DoesNotExist:
# 		return redirect('/')

# 	return render(request, 'pints_main/brewery_detail.html', context_dict)

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