from django.db import models
from accounts.models import User

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username