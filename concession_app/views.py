from django.shortcuts import render

# Create your views here.





def index(request):

    return render(request, '')


def login(request):

    if request.method == "POST":
        print("login")
        print("data :: ", request.POST)


    return render(request, 'login.html')


def register(request):

    if request.method == "POST":
        print("register")
        print("data :: ", request.POST)

        

    return render(request, 'signup.html')


