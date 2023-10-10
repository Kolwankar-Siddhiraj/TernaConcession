from django.http import HttpResponse
from django.shortcuts import redirect
from concession_app.models import *


def admin(Wrapped):
    def wrapper(request, *args, **kwargs):
        
        print(f'User :: {request.user}')
        if request.user.is_authenticated:
            if request.user.user_type == "admin":
                return Wrapped(request, *args, **kwargs)
            else:
                return HttpResponse('UnAuthorized', status=403)
        else:
            return HttpResponse('Not Allowed', status=401)

    return wrapper


def student(Wrapped):
    def wrapper(request, *args, **kwargs):
        
        print(f'User :: {request.user}')
        if request.user.is_authenticated:
            if request.user.user_type == "student":
                return Wrapped(request, *args, **kwargs)
            else:
                return HttpResponse('UnAuthorized', status=403)
        else:
            return HttpResponse('Not Allowed', status=401)

    return wrapper


def no_auth(Wrapped):
    def wrapper(request, *args, **kwargs):
        
        print(f'User :: {request.user}')
        if not request.user.is_authenticated:
            return Wrapped(request, *args, **kwargs)
        else:
            if request.user.user_type == "student":
                return redirect('/s/dashboard')
            if request.user.user_type == "admin":
                return redirect('/a/dashboard')
            
            return HttpResponse('Not Allowed', status=401)

    return wrapper





