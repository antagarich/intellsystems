from django.conf.urls import patterns, include, url
from django.contrib import admin
from GeneticAlgorithms import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.Beginning.as_view()),
    url(r'ga/', views.GA.as_view()),
    url(r'ga/config/', views.genetic_init_config)
)

url('^step', views.genetic_step),
url('^clear', views.genetic_clear),