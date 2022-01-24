"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from fileinput import filename
from http.client import HTTPResponse
from nturl2path import pathname2url
import pathlib
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib import admin
from django.urls import URLPattern, path
from django.views import View
from home import views
import random
import os
import urllib.request
import random

urlpatterns = [
    path ("index",views.index,name= "index"),
    path("vegan_icecream",views.vegan_icecream, name = "vegan_icecream"),
    path("menu", views.menu, name = 'menu'),
    path("about",views.about,name = 'about'),
    path("services",views.services, name = 'services'),
    path("contact",views.contact, name = 'contact')

]

