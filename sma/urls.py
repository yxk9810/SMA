from django.conf.urls import url

from . import views

urlpatterns = [
		url(r'^$', views.index, name='index'),
		url(r'dataset', views.dataset, name='dataset'),
		url(r'paper', views.paper, name='paper'),
		url(r'about', views.about, name='about'),
		url(r'keywords', views.keywords, name='keywords'),
		url(r'annotation/(?P<questionid>\d+)/$', views.annotation, name='annotion'),
		url(r'label', views.label, name='label'),
		url(r'signin', views.signin, name='signin'),
		url(r'login', views.login, name='login'),
		url(r'logout', views.logout, name='logout'),



]
