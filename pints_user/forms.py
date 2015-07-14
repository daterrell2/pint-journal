from django import forms
from pints_user.models import UserProfile
from django.contrib.auth.models import User

class UserForm(forms.Form):
	username = forms.CharField(label='Username')
	email = forms.EmailField(label = 'Email')
	password1 = forms.CharField(widget=forms.PasswordInput(), label = 'Password')
	password2 = forms.CharField(widget=forms.PasswordInput(), label = 'Verify Password')
	picture = forms.ImageField(label = 'Profile Picture', required=False)

	def clean_username(self):
		u = self.cleaned_data['username']
		if User.objects.filter(username=u):
			raise forms.ValidationError("Username is already taken. Please enter a new name")

		return u

	def clean_password2(self):
		p1, p2 = self.cleaned_data['password1'], self.cleaned_data['password2']

		if not p2 or p2 != p1:
			raise forms.ValidationError("Your passwords don't match!")

		return p2




