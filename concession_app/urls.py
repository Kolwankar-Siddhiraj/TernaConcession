from django.urls import path
from concession_app.views import *
urlpatterns = [
    path('', index, name="index"),
    path('login', LoginView, name="login"),
    path('register', RegisterView, name="register"),
    
    
    # test
    path('test', test, name="test"),
]
