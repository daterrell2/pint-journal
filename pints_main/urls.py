from django.conf.urls import patterns, url
from pints_main import views

urlpatterns = patterns('',
	url(r'^$', views.main_page, name='main_page'),
	url(r'^brewery/(?P<brewery_name_slug>[\w\-]+)[\-\d\/]?$', views.brewery_detail, name = 'brewery_detail'),
	url(r'^brewery/(?P<brewery_name_slug>[\w\-]+)[\-\d]?/add_beer/?$', views.add_beer, name = 'add_beer'),
	url(r'^beer/(?P<beer_name_slug>[\w\-%]+)[\-\d\/]?$', views.beer_detail, name = 'beer_detail'),
	)