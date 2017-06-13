from django.conf.urls import url, include
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^db436f59fd7104428cc5ec9268dbc0a4d939e458d1316f425e/?$', views.webhook.as_view()),
]