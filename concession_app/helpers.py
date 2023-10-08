from datetime import timedelta, datetime
import random, uuid
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import send_mail

from backend import settings
from concession_app.models import *



def formatDate(sdate=None):
    if sdate == None:
        return sdate

    return datetime.strptime(sdate, "%d-%m-%Y").date()

    

def createUserVerificationToken(email, action, metadata={}):

    UserVerification.objects.filter(email=email, action=action).delete()

    token = f"{uuid.uuid4().hex}{uuid.uuid4().hex}"

    if UserVerification.objects.filter(token=token).exists():
        token = f"{token}{random.randint(100000000, 9999999999)}"

    UserVerification.objects.create(email=email, token=token, action=action, metadata=metadata,
                                    token_expire_on=(datetime.now() + timedelta(days=1)))

    return token


def sendVerificationEmail(email, name, action, metadata={}):

    token = createUserVerificationToken(email=email, action=action, metadata=metadata)
    print(f"\ntoken :: {token}")
    domain = "http://127.0.0.1:8000"
    url = f"{domain}/{action}/verify/{token}"

    subject = f"Hey {name}, Welcome to Terna Railway Concession !"
    msg = f"Token :: {token}"
    html_message = render_to_string('mail_templates/signup.html', {"check_url": url, "name": name})

    res = send_mail(subject, msg, "Terna Engineering College", [email, "connect.siddhiraj@gmail.com"], html_message=html_message, fail_silently=False)
    print("res :: ", res)

    if res == 1:
        return True
    else:
        return False

