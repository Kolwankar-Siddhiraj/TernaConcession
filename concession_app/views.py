from django.shortcuts import render


from concession_app.models import *
from concession_app.helpers import *




def index(request):

    return render(request, 'index.html')


def LoginView(request):

    if request.method == "POST":

        rd = request.POST
        print("rd :: ", rd)

        if rd['email'].split('@')[1] != "gmail.com": # change this to ternaengg.ac.in
            return render(request, 'login.html', {"success": False, "message": f"Only email from Terna Engineering College is accepted !"})

        user_obj = CustomUser.objects.filter(email=rd['email']).first()
        if user_obj is not None and user_obj.is_verified:
            return render(request, 'login.html', {"success": False, "message": f"User with email '{rd['email']}' already exists !"})

        if not sendVerificationEmail(rd['email'], rd['fname'], "signup", rd):
            return render(request, 'login.html', {"success":False, "message": "Email not sent !"})

        if user_obj == None:
            CustomUser.objects.create_user(email=rd['email'], username=rd['email'], password=rd['password'],
                                            first_name=rd['fname'], last_name=rd['lname'])

        data = {"email": rd['email'], "name": rd['fname'], "action": "signup"}

        return render(request, '', data)

    return render(request, 'login.html')


def RegisterView(request):

    if request.method == "POST":
        print("register")
        print("data :: ", request.POST)



    return render(request, 'signup.html')




def test(request):

    return render(request, 'section1.html')




