from django.conf.urls import patterns, url
from pints_main import views

urlpatterns = patterns('',
	url(r'^$', views.main_page, name='main_page'),
	url(r'^brewery/(?P<brewery_name_slug>[\w\-]+)/?$', views.brewery_detail, name = 'brewery_detail'),
	url(r'^brewery/add_beer/(?P<brewery_name_slug>[\w\-]+)/?$', views.add_beer, name = 'add_beer'),
	url(r'^beer/edit_beer/(?P<beer_name_slug>[\w\-]+)/?$', views.edit_beer, name = 'edit_beer'),
	url(r'^beer/delete_beer/(?P<beer_name_slug>[\w\-]+)/?$', views.delete_beer, name = 'delete_beer'),
	url(r'^beer/(?P<beer_name_slug>[\w\-]+)/?$', views.beer_detail, name = 'beer_detail'),
	)