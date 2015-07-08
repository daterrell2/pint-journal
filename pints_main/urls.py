from django.conf.urls import patterns, url
from pints_main import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^welcome/?$', views.welcome, name='welcome'),
	url(r'^beer/(?P<beer_id>[\w\-]+)/?$', views.beer_detail, name = 'beer_detail'),
	url(r'^beer/(?P<beer_id>[\w\-]+)/add_score/?$', views.beer_detail, name = 'add_score'),
	url(r'^brewery/(?P<brewery_id>[\w\-]+)/?$', views.brewery_detail, name = 'brewery_detail'),
	url(r'^search/', views.search, name = 'search')
	# url(r'^brewery/add_beer/(?P<brewery_name_slug>[\w\-]+)/?$', views.add_beer, name = 'add_beer'),
	# url(r'^beer/edit_beer/(?P<beer_name_slug>[\w\-]+)/?$', views.edit_beer, name = 'edit_beer'),
	# url(r'^beer/delete_beer/(?P<beer_name_slug>[\w\-]+)/?$', views.delete_beer, name = 'delete_beer'),
	)