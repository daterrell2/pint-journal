from django.shortcuts import render, redirect
from pints_user.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def register(request):

	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True

			# authenticate and log in new user
			new_user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
			try:
				login(request, new_user)
				# replace with redirect to welcome page
				return redirect('pints_main.views.index')

			except:
				return redirect('user_login')

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,
			'pints_user/register.html',
			{'user_form' : user_form, 'profile_form' : profile_form, 'registered' : registered})

def user_login(request):

	#redirect if user is already logged in
	if request.user.is_authenticated():
		return redirect('pints_main.views.index')


	username, error_message = '', ''

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		next = request.POST.get('next')

		# built-in django user authentication

		user = authenticate(username=username, password=password)

		if user:
			#valid user and active account: log in and redirect to referer
			if user.is_active:
				login(request, user)
				if next:
					return redirect(next)
				else:
					return redirect('pints_main.views.main_page')

			# inactive account
			else:
				redirect('pints_main.welcome')
		# invalid credentials
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			error_message = 'Invalid Login'
			return render(request, 'pints_user/login.html', {'username' : username, 'error_message' : error_message, "next" : next})

	else:
		# initial GET request. 'next' will be hidden input on login form
		next = request.GET.get('next')
		if not next:
			next = '/'

		return render(request, 'pints_user/login.html', {'username' : username, 'error_message' : error_message, 'next' : next })

@login_required
def user_logout(request):

	logout(request)
	return redirect('pints_main.views.welcome')




