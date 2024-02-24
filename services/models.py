from django.db import models
from accounts.models import MyUser

class Department(models.Model):
    department_name = models.CharField( max_length=100)
    department_number = models.CharField(max_length=20)
    chairperson = models.ForeignKey(MyUser, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()
    
class Complaint(models.Model):
    
    status_choices = (
        ('Pending','Pending'),
        ('Solved', 'Solved')
    )
    
    message = models.TextField()
    status = models.CharField(max_length = 20, choices=status_choices, default='Pending')
    file = models.FileField(upload_to="complaints", blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    sender = models.ForeignKey(MyUser, related_name='Sender', on_delete=models.CASCADE)

class Feedback(models.Model):
    complaint = models.ForeignKey(Complaint, related_name='Complaint', on_delete=models.CASCADE)
    message = models.TextField()
    file = models.FileField(upload_to='Feedbacks', blank=True, null=True)
    images = models.ImageField(upload_to='images', blank=True, null=True)

# Create your models here.
