from django.contrib import admin
from pints_main.models import BeerScore, BeerScoreArchive

# class BreweryAdmin(admin.ModelAdmin):
# 	prepopulated_fields = {'slug':('name',)}

# class BeerAdmin(admin.ModelAdmin):
# 	prepopulated_fields = {'slug':('brewery', 'name')} 

class BeerScoreAdmin(admin.ModelAdmin):
	list_display = ['beer', 'score', 'score_date', 'user']

class BeerScoreArchiveAdmin(admin.ModelAdmin):
	list_display = ['beer', 'score', 'score_date', 'user']

# admin.site.register(Brewery, BreweryAdmin)
# admin.site.register(Beer, BeerAdmin)
admin.site.register(BeerScore, BeerScoreAdmin)
admin.site.register(BeerScoreArchive, BeerScoreArchiveAdmin)
