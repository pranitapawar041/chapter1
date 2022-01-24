from django.shortcuts import render, HttpResponse
import requests



# Create your views here.
def index(request):
    context = {
        #"variable1":"users data1",
        #"variable2":"users data2"
    }
    return render (request,'index.html',context)
    # return HttpResponse("the the first page!")
#def header(request):
    #wishes = {"first":"welcome Everyone"}
   # return render (request,'index.html',wishes)
    #return HttpResponse("header is here")
def vegan_icecream(request):
    #return HttpResponse("welcome to our icecream parlour")
    return render(request,'index.html')
def menu(request):
    return HttpResponse("Here is what we serve")
def about(request):
    return HttpResponse("all about us")
def services (request):
    return HttpResponse("You better taste below things")
def contact (request):
    return HttpResponse("reach out to us here!")