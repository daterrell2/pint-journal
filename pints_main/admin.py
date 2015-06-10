from django.contrib import admin
from pints_main.models import Brewery, Beer, Beer_Score

class BreweryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}

class BeerAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('brewery', 'name')} 

class Beer_ScoreAdmin(admin.ModelAdmin):
	list_display = ['beer', 'score', 'score_date']

admin.site.register(Brewery, BreweryAdmin)
admin.site.register(Beer, BeerAdmin)
admin.site.register(Beer_Score, Beer_ScoreAdmin)
