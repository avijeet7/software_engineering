from django.conf.urls import url

from course import views

urlpatterns = [
    url(r'^list/', views.list, name='course'),
]