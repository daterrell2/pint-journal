from django.conf.urls import patterns, url
from pints_main import views

urlpatterns = patterns('',
	url(r'^$', views.main_page, name='main_page'),
	url(r'^brewery/(?P<brewery_name_slug>[\w\-]+)/?$', views.brewery_detail, name = 'brewery_detail'),
	url(r'^brewery/(?P<brewery_name_slug>[\w\-]+)/add_beer/?$', views.add_beer, name = 'add_beer'),
	url(r'^beer/(?P<beer_name_slug>[\w\-]+)/edit_beer/?$', views.edit_beer, name = 'edit_beer'),
	url(r'^beer/(?P<beer_name_slug>[\w\-]+)/delete_beer/?$', views.delete_beer, name = 'delete_beer'),
	url(r'^beer/(?P<beer_name_slug>[\w\-]+)/?$', views.beer_detail, name = 'beer_detail'),
	)