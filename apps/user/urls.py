from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^login/process$', views.loginP),
    url(r'^register/process$', views.regiP),
    url(r'^userinfo', views.show),
]