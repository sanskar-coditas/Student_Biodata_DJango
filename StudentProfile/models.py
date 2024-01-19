from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - DOB: {self.dob}, Photo: {self.photo}, Resume: {self.resume}'
