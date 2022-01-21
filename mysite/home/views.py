from django.shortcuts import render, HttpResponse
import requests



# Create your views here.
def index(request):
    context = {
        "variable1":"users data1",
        "variable2":"users data2"
    }
    return render (request,'index.html',context)
    # return HttpResponse("the the first page!")
def header(request):
    wishes = {"first":"welcome Everyone"}
    return render (request,'index.html',wishes)
    #return HttpResponse("header is here")
def content(request):
    context = {
        "var1": "heyyyyyyyyyyyyyyyyyyyy ",
        "var2": "lets play cricket"
    }
    return render (request,'index.html',context)
def details(request):
    return HttpResponse("details about the user")
def end(request):
    return HttpResponse("The end!")
     