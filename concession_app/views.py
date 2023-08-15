from django.shortcuts import render

# Create your views here.





def index(request):

    return render(request, '')


def login(request):

    if request.method == "POST":
        print("post")
        print("data :: ", request.POST)


    return render(request, 'login.html')


def register(request):

    if request.method == "POST":
        print("post")
        print("data :: ", request.POST)

    return render(request, 'signup.html')


