from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    context = {
        "variable1":"users data1",
        "variable2":"users data2"
    }
    return render (request,'index.html',context)
    # return HttpResponse("the the first page!")
def header(request):
    return HttpResponse("header is here")
def content(request):
    return HttpResponse("para is here")
def details(request):
    return HttpResponse("details about the user")
def end(request):
    return HttpResponse("The end!")
     