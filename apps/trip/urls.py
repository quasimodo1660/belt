from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^add$', views.add),
    url(r'^add/process', views.add_process),
    url(r'^join$', views.join),
    url(r'^destination/(?P<id>\d+)$', views.show),
]