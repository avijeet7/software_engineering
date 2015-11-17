from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='instructor index'),
    url(r'^add_course/', views.add_course, name='Add Course'),
    url(r'^add_prereq/', views.add_prereq, name='Add Prerequisites'),
]