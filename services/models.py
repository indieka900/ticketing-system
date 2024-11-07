from django.db import models
from accounts.models import MyUser

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_number = models.CharField(max_length=20)
    description = models.TextField()
    
    def __str__(self):
        return self.department_name

class DepartmentChairperson(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='chair_department')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='chairs')
    date_assigned = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'department']  # Ensures one user can't be in multiple departments
        
    def __str__(self):
        return f"{self.user} - Chair of {self.department}"
    
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
    sender = models.ForeignKey(MyUser, related_name='feedback', on_delete=models.CASCADE)
    receiver = models.ForeignKey(MyUser, related_name='reciever', on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaint, related_name='Complaint', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    message = models.TextField()
    file = models.FileField(upload_to='Feedbacks', blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender} to {self.receiver}"

# Create your models here.
