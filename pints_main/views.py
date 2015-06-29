from django.shortcuts import render, redirect
from pints_main.models import Brewery, Beer, BeerScore
from pints_main.forms import BeerForm, BreweryForm, BeerScoreForm
from django.contrib.auth.decorators import login_required

def main_page(request):
	'''
	Looks for query string in url '?view=beer' or '?view=brewery' and renders
	main_page.html with appropriate object. Default view is 'beer'
	'''

	view = 'beer'
	brewery_list = []
	beer_list = []

	#check for params in url
	view_param = request.GET.get('view')
	if view_param and view_param == 'brewery':
		view = view_param
		# only query for breweries if asked
		brewery_list = Brewery.objects.order_by('-date_added')[:24]
	else:
		beer_list = Beer.objects.order_by('-date_added')[:24]

	context_dict = {'breweries': brewery_list, 'beers': beer_list, 'view': view}
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

	if request.method=='POST':
		form = BeerScoreForm(request.POST)

		if form.is_valid():
			if beer:
				score = form.save(commit=False)
				score.beer=beer
				score.save()

				form = BeerScoreForm() #new blank form

				return redirect('/beer/'+beer.slug)

		else:
			print form.errors

	else:
		form = BeerScoreForm()

	context_dict['form'] = form
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

@login_required
def add_brewery(request):
	if request.method=='POST':
		form = BreweryForm(request.POST)

		if form.is_valid():
			new_brewery = form.save(commit=True)
			return redirect('/brewery/'+new_brewery.slug)

		else:
			print form.errors

	else:
		form = BreweryForm()

	return render(request, 'pints_main/add_brewery.html', {'form':form})

@login_required
def add_beer(request, brewery_name_slug):
 
 	try:
		brewery = Brewery.objects.get(slug=brewery_name_slug)

	except Brewery.DoesNotExist:
		brewery = None

	if request.method=='POST':
		form = BeerForm(request.POST)

		if form.is_valid():
			if brewery:
				beer = form.save(commit=False)
				beer.brewery = brewery
				beer.save()

				return redirect('/beer/'+beer.slug)

		else:
			print form.errors

	else:
		form = BeerForm()

	context_dict={'form':form, 'brewery':brewery}

	return render(request, 'pints_main/add_beer.html', context_dict)

@login_required
def edit_beer(request, beer_name_slug):

	try:
		beer = Beer.objects.get(slug=beer_name_slug)

	except Beer.DoesNotExist:
		redirect('main_page')

	if request.method=='POST':
		form = BeerForm(request.POST, instance = beer)

		if form.is_valid():
				beer = form.save(commit=False)
				beer.save()
				return redirect(beer.get_absolute_url())

		else:
			print form.errors

	else:
		form = BeerForm(instance = beer)

	context_dict={'form':form, 'beer':beer}

	return render(request, 'pints_main/edit_beer.html', context_dict)

@login_required
def delete_beer(request, beer_name_slug):

	try:
		beer = Beer.objects.get(slug=beer_name_slug)
		brewery = beer.brewery

	except:
		redirect('main_page')

	if request.method=='POST':
		beer.delete()
		return redirect(brewery.get_absolute_url())
	else:
		return render(request, 'pints_main/delete_beer.html', {'beer':beer})