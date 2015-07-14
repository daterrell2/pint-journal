from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from pints_user.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import UserProfile


def register(request):

	registered = False

	if request.method == 'POST':
		form = UserForm(data=request.POST)
		#profile_form = UserProfileForm(data=request.POST)

		if form.is_valid():
			new_user = User()
			new_user.username = form.cleaned_data['username']
			new_user.email = form.cleaned_data['email']
			new_user.set_password(form.cleaned_data['password1'])
			new_user.save()


			if 'picture' in request.FILES:
				new_user_profile = UserProfile(user=new_user)
				new_user_profile.picture = request.FILES['picture']
				new_user_profile.save()

			registered = True

			# authenticate and log in new user
			user_login = authenticate(username=new_user.username,
									  password=request.POST.get('password1'))
			try:
				login(request, user_login)
				return redirect('pints_main.views.index')

			except:
				return redirect('user_login')

		else:
			print form.errors

	else:
		form = UserForm()

	return render(request,
			'pints_user/register.html',
			{'form' : form, 'registered' : registered})

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
		if not next or next == reverse(register):
			next = '/'

		return render(request, 'pints_user/login.html', {'username' : username, 'error_message' : error_message, 'next' : next })

@login_required
def user_logout(request):

	logout(request)
	return redirect('pints_main.views.welcome')




