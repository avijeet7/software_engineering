from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='registrar_home'),
    url(r'^add_inst/', views.add_inst, name='registrar'),
]