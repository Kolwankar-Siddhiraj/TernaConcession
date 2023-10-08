from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

# Create your models here.




class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username=None, password=None, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username=None, password=None, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        if username == None:
            username = email

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)

        if password is not None:
            user.set_password(password)

        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    STATUS_CHOICES = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('banned', 'banned'),
    )

    # user_type => student | admin
    user_type = models.CharField(max_length=25, default="student")
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True,null=True)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    # birth_date => {"date": 21, "month": 12, "year": 2023}
    birth_date = models.DateField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True,choices=STATUS_CHOICES)  # active, inactive, banned

    is_staff = models.BooleanField(default=False)
    
    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class StudentInfo(models.Model):

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    semester = models.CharField(max_length=10)
    student_id_no = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)


class ConcessionAdmin(models.Model):

    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department = ArrayField(models.CharField(max_length=100, null=True, blank=True), size=12)
    admin_id_no = models.CharField(max_length=100)


class TrainDetail(models.Model):

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    railway_line = models.CharField(max_length=25)
    # pass_period => monthly | quaterly
    pass_period = models.CharField(max_length=25, default="monthly")
    class_type = models.CharField(max_length=25, default="2nd")
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    route_via = models.CharField(max_length=30, null=True, blank=True)


class TicketDetail(models.Model):

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ticket_no = models.CharField(max_length=25)
    expiry_date = models.DateField(blank=True, null=True)
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)


class ConcessionApplication(models.Model):

    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # state => applied | in-progress | completed | rejected
    state = models.CharField(max_length=10, default="applied")

    # student info
    email = models.CharField(max_length=50)
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    # college details
    department = models.CharField(max_length=100)
    semester = models.CharField(max_length=10)
    student_id_no = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)

    # previous ticket details
    ptd_ticket_no = models.CharField(max_length=25)
    ptd_expiry_date = models.DateField(blank=True, null=True)
    ptd_source = models.CharField(max_length=30)
    ptd_destination = models.CharField(max_length=30)

    # train details
    railway_line = models.CharField(max_length=25)
    pass_period = models.CharField(max_length=25)
    class_type = models.CharField(max_length=25)
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    route_via = models.CharField(max_length=30, null=True, blank=True)


class UserVerification(models.Model):
    email = models.CharField(max_length=70, blank=True, null=True)
    token = models.CharField(unique=True, max_length=200, blank=True, null=True)
    # action => signup | forgotPasword | twoStepAuth | login 
    action = models.CharField(max_length=50, blank=True, null=True)
    token_expire_on = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.email


