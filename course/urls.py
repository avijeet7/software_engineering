from django.conf.urls import url

from course import views

urlpatterns = [
    url(r'^list/', views.list, name='course'),
    url(r'^add_inst/', views.add_inst, name='registrar'),
    url(r'^registrar/', views.registrar, name='registrar'),
    url(r'^instructor/', views.instructor, name='instructor'),
    url(r'^student/', views.student, name='instructor'),
]