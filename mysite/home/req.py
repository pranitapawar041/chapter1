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
