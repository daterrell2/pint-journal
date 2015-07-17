from django import forms
from pints_main.models import BeerScore

class BeerScoreForm(forms.ModelForm):
	#score = forms.IntegerField(help_text="Score", label="Score", initial="100")

	class Meta:
		model = BeerScore
		fields = ('score',)
		widgets = {
		'score' : forms.NumberInput(
			attrs={'id':'score-val', 'required': True, 'placeholder':'score'}
			),
		}
		




