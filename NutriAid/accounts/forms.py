from django import forms
from django.contrib.auth.forms import authenticate

from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Email or Password is incorrect")


class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address')
    name = forms.CharField(max_length=60)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        help_text='Password must contain at least 8 character including numeric values',
    )

    class Meta:
        model = UserModel
        fields = ("name", "email", "password1", "password2")


class NutritionistRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address')
    name = forms.CharField(max_length=60)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        help_text='Password must contain at least 8 character including numeric values',
    )

    class Meta:
        model = UserModel
        fields = ("name", "email", "password1", "password2")


class NutritionistProfileUpdateForm(ModelForm):
    image = forms.ImageField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
    )

    class Meta:
        model = NutritionistModel
        fields = '__all__'
        exclude = ['user']


class PatientProfileUpdateForm(ModelForm):
    image = forms.ImageField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
    )
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))  # date of birth

    class Meta:
        model = PatientModel
        fields = '__all__'
        exclude = ['user']


class PatientAppointmentForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = AppointmentModel
        fields = '__all__'
        exclude = ['patient', 'nutritionist', 'time', 'meet_link', 'is_accepted', 'is_canceled', 'is_completed',
                   'date_created']


class NutritionistAppointmentForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    meet_link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'https://meet.google.com/eig-xdgg-ixj'}))

    class Meta:
        model = AppointmentModel
        fields = '__all__'
        exclude = ['patient', 'nutritionist', 'is_accepted', 'is_canceled', 'is_completed',
                   'date_created']
