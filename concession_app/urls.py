from django.urls import path
from concession_app.views import *
urlpatterns = [
    path('', index, name="index"),
    path('login', LoginView, name="login"),
    path('register', RegisterView, name="register"),
    path('<str:action>/verify/<str:token>', VerifyUserView, name="verify-user"),
    path('verified', Verified, name="verified"),


    # student
    path('personal-details', PersonalDetailsView, name="personal-details"),
    path('college-details', CollegeDetailsView, name="college-details"),
    path('train-details', TrainDetailsView, name="train-details"),
    path('ticket-details', TicketDetailsView, name="train-details"),
    path('homepage', Homepage, name="homepage"),
    path('apply-concession', ApplyConcessionView, name="apply-concession"),
    path('s/dashboard', StudentDashboard, name="student-dashboard"),

    
    # test
    path('test', test, name="test"),
]
