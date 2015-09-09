from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^view/', views.view, name='homepage'),
    url(r'^delete/', views.delete, name='delete course'),
    url(r'^add/', views.add, name='add course'),
]