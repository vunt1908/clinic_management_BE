from django.db import models
from doctor.models import Doctor
from patient.models import Patient
from datetime import datetime

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('examining', 'Examining'),
        ('awaiting_clinical_results', 'Awaiting clinical results'),
        ('paraclinical_results_available', 'Paraclinical results available'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    TIME_SLOTS = [
        "07:30-08:30", "08:30-09:30", "09:30-10:30", 
        "10:30-11:30", "13:30-14:30", "14:30-15:30", 
        "15:30-16:30", "16:30-17:30", "18:00-19:00", 
        "19:00-20:00", "20:00-21:00"
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    time_slot = models.CharField(max_length=20, choices=[(slot, slot) for slot in TIME_SLOTS])
    date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'date', 'time_slot')

    def __str__(self):
        return self.time_slot + ' ' + self.date.strftime('%Y-%m-%d')
    @staticmethod
    def get_available_slots(doctor_id, date):
        try:
            day_of_week = datetime.strptime(date, '%Y-%m-%d').weekday()
            all_slots = Appointment.TIME_SLOTS

            if day_of_week in [5, 6]: 
                all_slots = all_slots[:8] 

            booked_slots = Appointment.objects.filter(
                doctor_id=doctor_id,
                date=date,
                status__in=['pending', 'confirmed', 'examining', 'awaiting_clinical_results', 'paraclinical_results_available']
            ).values_list('time_slot', flat=True)

            return [slot for slot in all_slots if slot not in booked_slots]

        except ValueError:
            raise ValueError("Ngày không hợp lệ.")
        
