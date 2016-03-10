from django.conf.urls import url

from . import views

urlpatterns = [
		url(r'^$', views.index, name='index'),
		url(r'dataset', views.dataset, name='dataset'),
		url(r'paper', views.paper, name='paper'),
		url(r'about', views.about, name='about'),
		url(r'keywords', views.keywords, name='keywords'),


]
