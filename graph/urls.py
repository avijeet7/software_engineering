from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.graph, name='graph'),
    url(r'^api/', views.graph_data, name='graph'),
]