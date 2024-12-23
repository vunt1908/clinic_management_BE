from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    department_image = models.ImageField(upload_to='department_images/', null=True, blank=True)

    def __str__(self):
        return self.name
    
