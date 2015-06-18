from django import forms
from pints_main.models import  Brewery, Beer, BeerScore, UserProfile
from django.contrib.auth.models import User

class BreweryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Brewery Name")
	country = forms.CharField(max_length=128, help_text="Country")
	brew_type = forms.CharField(max_length=128, help_text="Brewery Type")
	url = forms.URLField(max_length=200, help_text="url")
	slug = forms.SlugField(widget=forms.HiddenInput())
	date_added = forms.DateTimeField(widget=forms.HiddenInput())
	date_modified = forms.DateTimeField(widget=forms.HiddenInput())

	class Meta:
		model = Brewery
		fields = ('name', 'country', 'brew_type', 'url')

	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		if url and not url.startswith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url

		return cleaned_data

class BeerForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Beer Name")
	beer_style = forms.CharField(max_length=128, help_text="Style")
	slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Beer
		fields = ('name', 'beer_style')

class BeerScoreForm(forms.ModelForm):
	score = forms.IntegerField(help_text="Score")

	class Meta:
		model = BeerScore
		fields = ('score',)

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('picture',)
		




