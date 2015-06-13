from django.conf.urls import patterns, url
from pints_main import views

urlpatterns = patterns('',
	url(r'^$', views.main_page, name='main_page'),
	url(r'^brewery/(?P<brewery_name_slug>[\w\-]+)/?$', views.brewery_detail, name = 'brewery_detail'),
	url(r'^beer/(?P<beer_name_slug>[\w\-]+)/?$', views.beer_detail, name = 'beer_detail'),
	)