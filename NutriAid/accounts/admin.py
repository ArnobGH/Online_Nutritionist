from django.contrib import admin

from .models import *

admin.site.register(UserModel)
admin.site.register(NutritionistModel)
admin.site.register(PatientModel)
admin.site.register(SpecializationModel)
admin.site.register(AppointmentModel)
admin.site.register(ContactModel)
