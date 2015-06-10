from django.conf.urls import patterns, url
from pints_main import views

urlpatterns = patterns('',
	url(r'^$', views.main_page, name='main_page'),
	)