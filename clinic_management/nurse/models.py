from django.db import models
from accounts.models import User

class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username