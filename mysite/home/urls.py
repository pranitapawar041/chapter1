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
from ssl import ALERT_DESCRIPTION_DECODE_ERROR
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib import admin
from django.urls import path
from home import views
import random
import os
def put_file(req: HttpRequest):
    print(req.body)
    filename = "out.txt" + str(random.random())
    with open(filename, 'wb') as output:
        output.write(req.body)
    resp = {
        "success": True,
        "filename": filename
    }
    return JsonResponse(resp)
def get_file(req: HttpRequest, filename):
    print(filename)
    with open("uploads/ " + filename, 'rb') as f:
        content = f.read()
        print(content)
        return HttpResponse(content)

def delete_file(req:HttpRequest,filename):
    print(filename)
    if os.path.isfile(filename):
        os.remove(filename)
    deleted =  HttpResponse("file deleted")
    return deleted

# Get the path of current working directory
pathname = os.getcwd()
def list_file(req:HttpRequest):
    dir_list = os.listdir(pathname) 
    dir_list =HttpResponse(dir_list)
    return dir_list

urlpatterns = [
    path(" ", views.index, name = 'home'),
    path("index",views.index, name = "index"),
    path("header", views.header, name = 'header'),
    path("details",views.details, name = 'details'),
    path("end", views.end, name = 'end'),
    path('data', put_file),
    path('uploads/data/<filename>', get_file),
    path('uploads/data/<filename>',delete_file),
    path('uploads',list_file)
]

