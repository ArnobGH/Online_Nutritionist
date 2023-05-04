from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *


def home(request):
    user = request.user
    context = {}
    if user.is_authenticated and user.is_nutritionist:
        nutritionist = NutritionistModel.objects.get(user=user)

        context = {
            'nutritionist': nutritionist,
        }
    elif user.is_authenticated and user.is_patient:
        patient = PatientModel.objects.get(user=user)

        context = {
            'patient': patient,
        }
    return render(request, 'index.html', context)


def login_view(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user and user.is_patient:
                login(request, user)
                return redirect('home')
            elif user and user.is_nutritionist:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Email or Password is incorrect.')
                return redirect('login')
        else:
            return render(request, 'login.html', {'form': form})

    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def patient_register_view(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            user.is_patient = True
            user.save()
            PatientModel.objects.create(user=user)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'patient-registration.html', {"form": form})

    form = PatientRegistrationForm()
    context = {
        "form": form
    }
    return render(request, 'patient-registration.html', context)


def nutritionist_register_view(request):
    if request.method == 'POST':
        form = NutritionistRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            user.is_nutritionist = True
            user.save()
            NutritionistModel.objects.create(user=user)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'nutritionist-registration.html', {"form": form})

    form = NutritionistRegistrationForm()
    context = {
        "form": form
    }
    return render(request, 'nutritionist-registration.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def patient_profile(request, pk):
    user = UserModel.objects.get(id=pk)

    profile = PatientModel.objects.get(user=user)

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'patient-profile.html', context)


@login_required(login_url='login')
def nutritionist_profile(request, pk):
    user = UserModel.objects.get(id=pk)

    profile = NutritionistModel.objects.get(user=user)

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'nutritionist-profile.html', context)


@login_required(login_url='login')
def patient_edit_profile(request):
    profile = PatientModel.objects.get(user=request.user)

    form = PatientProfileUpdateForm(instance=profile)
    if request.method == 'POST':
        form = PatientProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('patient-profile', request.user.id)
        else:
            print(form.errors)
            return redirect('patient-edit-profile')

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'patient-edit-profile.html', context)


@login_required(login_url='login')
def nutritionist_edit_profile(request):
    profile = NutritionistModel.objects.get(user=request.user)

    form = NutritionistProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = NutritionistProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('nutritionist-profile', request.user.id)
        else:
            print(form.errors)
            return redirect('nutritionist-edit-profile')

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'nutritionist-edit-profile.html', context)


@login_required(login_url='login')
def nutritionists_list(request):
    nutritionists = NutritionistModel.objects.all()
    context = {
        'nutritionists': nutritionists,
    }
    return render(request, 'appointments/nutritionists.html', context)


def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email_add = request.POST['email']
        message = request.POST['message']
        ContactModel.objects.create(name=name, email=email_add, message=message)

        messages.success(request, "Feedback sent successfully.")

        return render(request, 'contact.html')

    return render(request, 'contact.html')


def patient_appointment_home_view(request):
    user = request.user 
    patient = PatientModel.objects.get(user=user) 
    appointments = AppointmentModel.objects.filter(patient=patient) 
    pending_appointments = [appointment for appointment in appointments
                            if appointment.is_accepted == False
                            and appointment.is_canceled == False
                            and appointment.is_completed == False] 
    upcoming_appointments = [appointment for appointment in appointments
                             if appointment.is_accepted == True
                             and appointment.is_canceled == False
                             and appointment.is_completed == False] 
    rejected_appointments = [appointment for appointment in appointments
                             if appointment.is_accepted == False
                             and appointment.is_canceled == True
                             and appointment.is_completed == False]  
    completed_appointments = [appointment for appointment in appointments
                              if appointment.is_accepted == True
                              and appointment.is_canceled == False
                              and appointment.is_completed == True] 

    context = { 
        'pending_appointments': pending_appointments,
        'upcoming_appointments': upcoming_appointments,
        'rejected_appointments': rejected_appointments,
        'completed_appointments': completed_appointments,
    }
    return render(request, 'appointments/patient-appointment-home.html', context)


def nutritionist_appointment_home_view(request):
    user = request.user 
    nutritionist = NutritionistModel.objects.get(user=user)  
    appointments = AppointmentModel.objects.filter(nutritionist=nutritionist)
    pending_appointments = [appointment for appointment in appointments
                            if appointment.is_accepted == False
                            and appointment.is_canceled == False
                            and appointment.is_completed == False] 
    upcoming_appointments = [appointment for appointment in appointments
                             if appointment.is_accepted == True
                             and appointment.is_canceled == False
                             and appointment.is_completed == False]  
    rejected_appointments = [appointment for appointment in appointments
                             if appointment.is_accepted == False
                             and appointment.is_canceled == True
                             and appointment.is_completed == False] 
    completed_appointments = [appointment for appointment in appointments
                              if appointment.is_accepted == True
                              and appointment.is_canceled == False
                              and appointment.is_completed == True]  
    context = { 
        'pending_appointments': pending_appointments,
        'upcoming_appointments': upcoming_appointments,
        'rejected_appointments': rejected_appointments,
        'completed_appointments': completed_appointments,
    }
    return render(request, 'appointments/nutritionist-appointment-home.html', context)


def appointment_detail_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)  
    is_pending = False  
    if appointment.is_accepted == False and appointment.is_canceled == False and appointment.is_completed == False:
        
        is_pending = True  

    is_upcoming = False  
    if appointment.is_accepted == True and appointment.is_canceled == False and appointment.is_completed == False:
       
        is_upcoming = True  

    is_completed = False  
    if appointment.is_completed: 
        is_completed = True  

    is_canceled = False
    if appointment.is_accepted == False and appointment.is_canceled == True and appointment.is_completed == False:
        is_canceled = True

    if request.GET.get('completeAppointment'):
        appointment.is_completed = True
        appointment.save()
        return redirect('appointment-details', appointment.id)

    context = {  
        'appointment': appointment,
        'is_pending': is_pending,
        'is_completed': is_completed,
        'is_upcoming': is_upcoming,
        'is_canceled': is_canceled,
    }
    return render(request, 'appointments/appointment-details.html', context)


def make_appointment_view(request, pk):
    nutritionist = NutritionistModel.objects.get(user=UserModel.objects.get(id=pk))  
    patient = PatientModel.objects.get(user=request.user)  

    form = PatientAppointmentForm()  
    if request.method == 'POST':  
        form = PatientAppointmentForm(request.POST)  
        if form.is_valid():  
            new_appointment = form.save(commit=False)  
            new_appointment.patient = patient  
            new_appointment.nutritionist = nutritionist  
            new_appointment.save()  
            return redirect('appointment-details', new_appointment.id)  
        else: 
            context = {  
                'patient': patient,
                'nutritionist': nutritionist,
                'form': form,
            }
            return render(request, 'pages/appointment/make-appointment.html', context)

    context = { 
        'patient': patient,
        'nutritionist': nutritionist,
        'form': form,
    }
    return render(request, 'appointments/make-appointment.html', context)


def doctor_appointment_update_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)  
    form = NutritionistAppointmentForm(instance=appointment)  
    if request.method == 'POST':  
        form = NutritionistAppointmentForm(request.POST, instance=appointment)  
        if form.is_valid():  
            appointment = form.save()  
            appointment.is_accepted = True  
            appointment.save() 
            return redirect('appointment-details', appointment.id)  

    context = { 
        'appointment': appointment,
        'form': form
    }
    return render(request, 'appointments/nutritionist-update-appointment.html', context)


def patient_appointment_update_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk) 
    form = PatientAppointmentForm(instance=appointment)  
    if request.method == 'POST':  
        form = PatientAppointmentForm(request.POST, instance=appointment)  
        if form.is_valid():  
            appointment.save()  
            return redirect('appointment-details', appointment.id)  

    context = {  
        'appointment': appointment,
        'form': form
    }
    return render(request, 'appointments/patient-update-appointment.html', context)


def appointment_delete_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)  

    if request.method == 'POST': 
        appointment.delete() 
        return redirect('patient-appointment-home')  

    context = {  
        'appointment': appointment,
    }
    return render(request, 'appointments/delete-appointment.html', context)  


def appointment_reject_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)  

    if request.method == 'POST':  
        appointment.is_canceled = True  
        appointment.save()  
        return redirect('appointment-details', appointment.id)  

    context = {  
        'appointment': appointment,
    }
    return render(request, 'appointments/reject-appointment.html', context)




def calculate(request):

    return render(request, 'calc.html')
#def calc(request):

#    context={'users':'1'}
#    return render(request, 'accounts/calc.html',context ) 


def biPage(request):
    return render(request, 'bmi.html')


def bmiresult(request):

    h = float(request.POST['height'])
    w = float(request.POST['weight'])
    bmi = (w/(h**2))*703

    if(bmi < 16):
        return render(request, 'result.html', {'result': (bmi, " Your Weight is Severely Underweight")})
    
    elif(bmi >= 16 and bmi < 18.5):
        return render(request, 'result.html', {'result': (bmi, " Your Weight is Underweight")})
    
    elif(bmi >= 18.5 and bmi < 25):
        return render(request, 'result.html', {'result': (bmi, " Your Weight is Healthy")})
    
    elif(bmi >= 25 and bmi < 38):
        return render(request, 'result.html', {'result': (bmi, " Your Weight is Overweight")})
    
    elif(bmi >= 38):
        return render(request, 'result.html', {'result': (bmi, " Your Weight is Obese")})
    #context={'users':'2'}
    return render(request, 'result.html', {'result': bmi})  



def brPage(request):
    return render(request, 'bmr.html')


def mbmrresult(request):

    h = float(request.POST['height'])
    w = float(request.POST['weight'])
    a = int(request.POST['age'])
    wk = w / 2.2
    hc = h * 2.54
    result = int((10 * wk) + (6.25 * hc) - (5 * a) + 5)
    return render(request, 'mbmrres.html', {'result': result})  

    
def femalebmr(request):
    return render(request, 'femalebmr.html')


def fbmrresult(request):

    h = float(request.POST['height'])
    w = float(request.POST['weight'])
    a = int(request.POST['age'])
    wk = w / 2.2
    hc = h * 2.54
    result = int((10 * wk) + (6.25 * hc) - (5 * a) - 161)
    return render(request, 'fbmrres.html', {'result': result})


def malebmr(request):
    return render(request, 'malebmr.html')

  
