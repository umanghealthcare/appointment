from django.contrib import admin
from .models import User,Contact,Doctor_profile,Appointment,cancelappointmentaptient,doctorappointmentaptient,Transaction,HealthProfile
# Register your models here.
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Doctor_profile)
admin.site.register(Appointment)
admin.site.register(cancelappointmentaptient)
admin.site.register(doctorappointmentaptient)
admin.site.register(Transaction)
admin.site.register(HealthProfile)