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
print(pathname)
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
class details(View):
    url = 'http://example.com/'
    def get(self,request,url):
        req = urllib.Request(url)#give url here then call 
        content = urllib.urlopen(req)
        data = content.read()
        content.close()
        return HTTPResponse(url)
    def put(self,url):
        req = urllib.Request(url)#give url here then call 
        content = urllib.urlopen(req)
        data = content.write(req.body)
        print(data)
        resp = {
        "success": True,
        "filename": URLPattern
        }
        return JsonResponse(resp)
    def delete(self,url):
         file_delete = pathlib.Path(url)
         file_delete.unlink()
         deleted = HttpResponse("delete success!")
         return deleted

# Get the path of current working directory
    pathname = os.getcwd()
    print(pathname)
    def list_file(req:HttpRequest):
        dir_list = os.listdir(pathname2url) 
        dir_list =HttpResponse(",".join(dir_list))
        return dir_list


urlpatterns = [
    path(" ", views.index, name = 'home'),
    path("index",views.index, name = "index"),
    path("header", views.header, name = 'header'),
    path("details",views.details, name = 'details'),
    path("end", views.end, name = 'end'),
    path('data', details.put),
    path('uploads/data/<filename>', details.get),
    path('deleted/data/<filename>',details.delete),
    path('uploads',details.list_file)

]

