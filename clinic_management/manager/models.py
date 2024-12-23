from django.db import models
from accounts.models import User

class Manager(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)