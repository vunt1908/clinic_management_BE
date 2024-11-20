from django.contrib import admin
from accounts.models import User
from patient.models import Patient
from doctor.models import Doctor
from departments.models import Department
from manager.models import Manager
from staff.models import Staff
from appointments.models import Appointment
from medicalrecords.models import MedicalRecord
from payments.models import Payment

# Register your models here.
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Department)
admin.site.register(Manager)
admin.site.register(Staff)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Payment)
