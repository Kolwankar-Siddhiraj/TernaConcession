from django.urls import path
from concession_app import views, student_views, admin_views


urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
]
