from django.conf.urls import url

from authentication import views

urlpatterns = [
    url(r'^$', views.auth_login, name='login'),
    url(r'^logout/', views.auth_logout, name='logout'),
    url(r'^signup/', views.auth_signup, name='signup'),
]