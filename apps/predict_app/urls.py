from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^info$', views.info),
    url(r'^create$', views.create)
]