from concession_app.models import *
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings




def sendUserVerificationEmail(email, name, action):

    token = createUserVerificationToken(email=email, action=action)
    print(f"token :: {token}")
    domain = "http://127.0.0.1:8000"

    if action == "signup":
        url = f"{domain}/account/verify-user/{token}"

        subject = f"Welcome to CompanyName {name} !"
        msg = f"Hey {name} ! \nComplete your signup process by activating your account."
        html_message = render_to_string('mail_template/signup.html', {"check_url": url})

    elif action == "forgotPassword":

        password_reset_url = f"{domain}/account/verify-user/{token}"

        login_token = createUserVerificationToken(email=email, action="login")
        login_url = f"{domain}/account/verify-user/{login_token}"

        subject = f"Reset your password !"
        msg = f"Hey {name} ! \nyou forgot your password No worries! Reset your password now Or directly Login."
        html_message = render_to_string('mail_template/forgotPassword.html', {"password_reset_url": password_reset_url, "login_url":login_url})

    else:
        return False

    res = send_mail(subject, msg, settings.DEFAULT_FROM_EMAIL, [email, "siddhirajk77gmail.com"], html_message=html_message, fail_silently=False)
    print("res :: ", res)

    if res == 1:
        return True
    else:
        return False


def createUserVerificationToken(email, action):

    UserVerification.objects.filter(email=email, action=action).delete()

    token = f"{uuid.uuid4().hex}{uuid.uuid4().hex}"

    if UserVerification.objects.filter(token=token).exists():
        token = f"{token}{random.randint(100000000, 9999999999)}"

    new_token = UserVerification.objects.create(email=email, token=token, action=action, expire_on=(datetime.now() + timedelta(days=1)))
    new_token.save()

    return token




