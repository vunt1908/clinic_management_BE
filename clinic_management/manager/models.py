from django.db import models
from accounts.models import User

# Create your models here.
class Manager(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)