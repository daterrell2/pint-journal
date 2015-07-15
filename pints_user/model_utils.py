from django.contrib.auth.models import User

def get_user(request):
	'''
	Takes Django request object and looks for authenticated user.
	Returns None or User object for authenticated user
	'''
	if not request.user.is_authenticated:
		user = None

	else:
		try:
			user=User.objects.get(id=request.user.id)
		except User.DoesNotExist:
			user = None

	return user