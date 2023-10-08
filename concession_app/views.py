from django.shortcuts import redirect, render
from django.contrib import auth

from concession_app.models import *
from concession_app.helpers import *




def index(request):

    return render(request, 'index.html')


def LoginView(request):

    if request.method == "POST":
        rd = request.data
        print("rd :: ", rd)

        user = auth.authenticate(email=rd['email'], password=rd['password'])
        print("user:",user)
        if user is not None:

            if not user.is_verified:
                return render(request, '', {"success": False, "message": "Email is not verified. Please verify Email and try Again !"})

            return render(request, '', {"success": True, "message": "User login successfully !", "data": None})
        else:
            return render(request, '', {"success": False, "message": "Oppps! Creadentials does not matched!"})

    return render(request, 'login.html')


def RegisterView(request):

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

        return render(request, 'student/checkmail.html', data)
        

    return render(request, 'signup.html')




def test(request):

    return render(request, '')



def VerifyUserView(request, action, token):

    UserVerification.objects.filter(token_expire_on__lte=datetime.now()).delete()

    token_obj = UserVerification.objects.filter(token=token, action=action, token_expire_on__gte=datetime.now()).first()

    if token_obj != None and action == "signup":

        user = CustomUser.objects.filter(email=token_obj.email).first()
        user.is_verified=True
        user.email_verified_at=datetime.now()
        user.save()

        auth.login(request, user)

        token_obj.delete()

        # return render(request, 'student/account_verified.html', {"success": True, "message": "User Verification successful !", "data": None})
        return redirect('/verified')

    else:
        return render(request, 'signup.html', {"success": False, "message": "Link has been expired!"})



def Verified(request):

    return render(request, 'student/account_verified.html')


def PersonalDetailsView(request):

    if request.method == "POST":

        rd = request.POST
        user = request.user
        print("rd :: ", rd)

        user_obj = CustomUser.objects.filter(email=user.email).first()
        rd['birth_date'] = formatDate(sdate=rd['birth_date'])

        user_obj.first_name = rd['first_name']
        user_obj.middle_name = rd['middle_name']
        user_obj.last_name = rd['last_name']
        user_obj.address = rd['address']
        user_obj.phone = rd['phone']
        user_obj.birth_date = rd['birth_date']

        user_obj.save()

        return redirect('/college-details')

    return render(request, 'section1.html')


def CollegeDetailsView(request):

    if request.method == "POST":
        rd = request.data
        user = request.user
        print("rd :: ", rd)

        student = StudentInfo.objects.filter(student__email=user.email).first()

        if student is not None:
            
            student.department = rd['department']
            student.semester = rd['semester']
            student.student_id_no = rd['student_id_no']
            student.roll_no = rd['roll_no']

            student.save()
            
        else:
            user_obj = CustomUser.objects.filter(email=user.email).first()
            student = StudentInfo.objects.create(student=user_obj, department=rd['department'], semester=rd['semester'],
                                                 student_id_no=rd['student_id_no'], roll_no=rd['roll_no'])
        
        return redirect('/train-details')

    return render(request, 'section2.html')


def TrainDetailsView(request):

    return render(request, 'student/account_verified.html')


def TicketDetailsView(request):

    return render(request, 'student/account_verified.html')






