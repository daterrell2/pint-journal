from django.conf.urls import patterns, url
from pints_main import views

urlpatterns = patterns('',
	url(r'^$', views.welcome, name='welcome'),
	url(r'^home/?$', views.index, name='index'),
	url(r'^beer/(?P<beer_id>[\w\-]+)/?$', views.beer_detail, name = 'beer_detail'),
	url(r'^beer/(?P<beer_id>[\w\-]+)/get_form/?$', views.get_form, name = 'get_form'),
	url(r'^beer/(?P<beer_id>[\w\-]+)/get_score/?$', views.get_score, name = 'get_score'),
	url(r'^beer/(?P<beer_id>[\w\-]+)/add_score/?$', views.add_score, name = 'add_score'),
	url(r'^brewery/(?P<brewery_id>[\w\-]+)/?$', views.brewery_detail, name = 'brewery_detail'),
	url(r'^search/', views.search, name = 'search'),
	)