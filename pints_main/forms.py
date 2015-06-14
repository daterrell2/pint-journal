from django import forms
from pints_main.models import  Brewery, Beer, Beer_Score

class BreweryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Enter the brewery name")
	country = forms.CharField(max_length=128, help_text="Enter country")
	brew_type = forms.CharField(max_length=128, help_text="What type of brewery is this?")
	url = forms.URLField(max_length=200, help_text="Enter the url")
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
	name = forms.CharField(max_length=128, help_text="Enter the name of the beer")
	beer_style = forms.CharField(max_length=128, help_text="What style is this beer")
	slug = forms.SlugField(widget=forms.HiddenInput(), required=False)
	#date_added = forms.DateTimeField(widget=forms.HiddenInput())
	#date_modified = forms.DateTimeField(widget=forms.HiddenInput())

	class Meta:
		model = Beer
		fields = ('name', 'beer_style')

class Beer_ScoreForm(forms.ModelForm):
	score = forms.IntegerField(help_text="Enter your score for this beer")
	#score_date = forms.DateTimeField(widget=forms.HiddenInput())

	class Meta:
		model = Beer_Score
		fields = ('score',)
