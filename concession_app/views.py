import json
from django.shortcuts import redirect, render
from django.contrib import auth
from django.forms.models import model_to_dict

from concession_app.models import *
from concession_app.helpers import *
from concession_app.access_decorators import *



def index(request):

    return render(request, 'index.html')


@no_auth
def LoginView(request):

    if request.method == "POST":
        rd = request.POST
        print("rd :: ", rd)

        user = auth.authenticate(email=rd['email'], password=rd['password'])
        print("user :: ", user)
        if user is not None:

            if not user.is_verified:
                return render(request, 'login.html', {"success": False, "message": "Email is not verified. Please verify Email and try Again !"})

            auth.login(request, user)

            if user.user_type == "student":
                return redirect('/s/dashboard')
            elif user.user_type == "admin":
                return redirect('/a/dashboard')
            else:
                return render(request, 'login.html', {"success": True, "message": "User login successfully !", "data": None})


            # if user.
        else:
            return render(request, 'login.html', {"success": False, "message": "Oppps! Creadentials does not matched!"})

    return render(request, 'login.html')


@no_auth
def RegisterView(request):

    if request.method == "POST":

        rd = request.POST
        print("rd :: ", rd)

        if rd['email'].split('@')[1] != "gmail.com": # change this to ternaengg.ac.in
            return render(request, 'signup.html', {"success": False, "message": f"Only email from Terna Engineering College is accepted !"})

        user_obj = CustomUser.objects.filter(email=rd['email']).first()
        if user_obj is not None and user_obj.is_verified:
            return render(request, 'signup.html', {"success": False, "message": f"User with email '{rd['email']}' already exists !"})

        if not sendVerificationEmail(rd['email'], rd['fname'], "signup", rd):
            return render(request, 'signup.html', {"success":False, "message": "Email not sent !"})

        if user_obj == None:
            CustomUser.objects.create_user(email=rd['email'], username=rd['email'], password=rd['password'],
                                            first_name=rd['fname'], last_name=rd['lname'])

        data = {"email": rd['email'], "name": rd['fname'], "action": "signup"}

        return render(request, 'student/checkmail.html', data)

    return render(request, 'signup.html')


def test(request):

    return render(request, 'section1.html')


@no_auth
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


@student
def Verified(request):

    return render(request, 'student/account_verified.html')


@student
def PersonalDetailsView(request):

    if request.method == "POST":

        rd = request.POST
        user = request.user
        print("rd :: ", rd)

        user_obj = CustomUser.objects.filter(email=user.email).first()
        # rd['birth_date'] = formatDate(sdate=rd['dob'])

        user_obj.first_name = rd['fname']
        user_obj.middle_name = rd['mname']
        user_obj.last_name = rd['lname']
        user_obj.address = rd['address']
        user_obj.phone = rd['phone']
        user_obj.birth_date = rd['dob']

        user_obj.save()

        return redirect('/college-details')

    return render(request, 'section1.html')


@student
def CollegeDetailsView(request):

    if request.method == "POST":
        rd = request.POST
        user = request.user
        print("rd :: ", rd)

        student = StudentInfo.objects.filter(student__email=user.email).first()

        if student is not None:

            student.department = rd['department']
            student.semester = rd['semester']
            student.student_id_no = rd['s_id']
            student.roll_no = rd['roll_no']

            student.save()

        else:
            user_obj = CustomUser.objects.filter(email=user.email).first()
            student = StudentInfo.objects.create(student=user_obj, department=rd['department'], semester=rd['semester'],
                                                 student_id_no=rd['s_id'], roll_no=rd['roll_no'])

        return redirect('/train-details')

    return render(request, 'section2.html')


@student
def TrainDetailsView(request):

    if request.method == "POST":

        rd = request.POST
        user = request.user
        print("rd :: ", rd)

        train_details = TrainDetail.objects.filter(student__email=user.email).first()

        if train_details is not None:

            train_details.railway_line = rd['line']
            train_details.class_type = rd['class']
            train_details.pass_period = rd['period']
            train_details.source = rd['source']
            train_details.destination = rd['destination']
            train_details.route_via = rd.get('route_via', None)

            train_details.save()

        else:
            user_obj = CustomUser.objects.filter(email=user.email).first()
            train_details = TrainDetail.objects.create(student=user_obj, railway_line=rd['line'], pass_period=rd['period'],
                                                        class_type=rd['class'], source=rd['source'], destination=rd['destination'],
                                                        route_via=rd.get('route_via', None))

        return redirect('/homepage')


    return render(request, 'section3.html')


@student
def Homepage(request):

    return render(request, 'student/initial_homepage.html')


@student
def ConcessionApplicationView(request):

    user = request.user

    if ConcessionApplication.objects.filter(applicant__email=user.email, state__in=["applied", "in-progress"]):
        return render(request, 'dashboard.html', {"success": False, "message": "Already one application is in progress !"})

    college_details = model_to_dict(StudentInfo.objects.filter(student__email=user.email).first())
    train_details = model_to_dict(TrainDetail.objects.filter(student__email=user.email).first())
    ticket = TicketDetail.objects.filter(student__email=user.email).order_by('id').last()
    user_obj = CustomUser.objects.filter(email=user.email).first()

    rd = {
        "applicant": user_obj,
        "email": user.email,
        "full_name": f"{user.first_name} {user.middle_name} {user.last_name}",
        "phone": user.phone,
        "address": user.address,
        "birth_date": user.birth_date,
        "ptd_ticket_no": ticket.ticket_no,
        "ptd_expiry_date": ticket.expiry_date,
        "ptd_source": ticket.source,
        "ptd_destination": ticket.destination
    }

    rd.update(college_details)
    rd.update(train_details)

    rd.pop('student')
    print("rdata :: ", rd)
    new_application = ConcessionApplication.objects.create(**rd)

    return redirect('/s/dashboard')


@student
def TicketDetailsView(request):

    if request.method == "POST":
        rd = request.POST
        user = request.user
        print("rd :: ", rd)

        ticket = TicketDetail.objects.filter(student__email=user.email, ticket_no=rd['tno']).first()

        if ticket == None:
            user_obj = CustomUser.objects.filter(email=user.email).first()
            new_ticket = TicketDetail.objects.create(student=user_obj, ticket_no=rd['tno'], expiry_date=rd['edate'],
                                                     source=rd['source'], destination=rd['destination'])

        return redirect('/apply-concession')

    return render(request, 'student/section4.html')


@student
def StudentDashboard(request):

    data = ConcessionApplication.objects.filter(applicant__email=request.user.email).order_by('-id').first()

    data = model_to_dict(data)
    print("data :: ", data)

    return render(request, 'student/student_dashboard.html', data)


@admin
def AdminDashbord(request):

    user = request.user
    print("user :: ", user)
    dep_admin = ConcessionAdmin.objects.filter(admin__email=user.email).first()
    applications = ConcessionApplication.objects.filter(department__in=dep_admin.department).values()

    print("applications :: ", applications)
    return render(request, 'admin/dashboard.html', {"applications": applications})


@admin
def ViewApplication(request, caid):

    ConcessionApplication.objects.filter(id=caid).update(state="in-progress") 
    application = model_to_dict(ConcessionApplication.objects.filter(id=caid).first())

    print("application :: ", application)

    return render(request, 'admin/view_application.html', application)


@admin
def ApplicationStatus(request, caid, status):

    if status in ["approved", "rejected"]:
        ca = ConcessionApplication.objects.filter(id=caid).first()
        ca.state=status
        ca.save()

        if sendApplicationStatusEmail(ca.email, (ca.full_name).split(" ")[0], status):
            return redirect('/a/dashboard')
        else:
            return redirect(f'/{caid}/view-application')


def LogoutView(request):

    auth.logout(request)
    return redirect('/login')



