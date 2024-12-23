from django.db import models

# Create your models here.
class Services(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
