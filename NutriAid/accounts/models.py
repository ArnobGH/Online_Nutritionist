from datetime import date

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


# User manager for the User Model
class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Must have an email address')

        if not name:
            raise ValueError('Must have a name')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


# User Model (Common for all the users)
class UserModel(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)  # Email
    name = models.CharField(max_length=255)  # Name
    is_patient = models.BooleanField(default=False)
    is_nutritionist = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # True if active
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Email & Password are required by default.

    objects = MyUserManager()  # User manager for the User Model

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class PatientModel(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)  # Patient Profile Picture
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    height = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.name

    def calc_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


class SpecializationModel(models.Model):
    specialization = models.CharField(max_length=50)

    def __str__(self):
        return self.specialization


class NutritionistModel(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True)
    specialization = models.ForeignKey(SpecializationModel, null=True, blank=True, on_delete=models.SET_NULL)


class AppointmentModel(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
    nutritionist = models.ForeignKey(NutritionistModel, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    meet_link = models.CharField(max_length=255, null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nutritionist.user.name


# Responses from Contact Us form will be saved here
class ContactModel(models.Model):
    name = models.CharField(max_length=255)  # name of the user
    email = models.CharField(max_length=255)  # email of the user
   
    message = models.TextField()  # message body
