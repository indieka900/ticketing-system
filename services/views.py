from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from services.models import (Complaint,Feedback,Department)

@login_required
def home(request):
    
    complaints = Complaint.objects.filter(sender = request.user)
    departments = Department.objects.all()
    
    if request.method == 'POST':
        if 'solved' in request.POST:
            id = request.POST.get('id')
            complaint = Complaint.objects.get(pk=id)
            complaint.status = 'Solved'
            complaint.save()
            #success message
            
        if 'transfer' in request.POST:
            id = request.POST.get('id')
            department = request.POST.get('department')
            complaint = Complaint.objects.get(pk=id)
            depart = Department.objects.get(pk=department)
            print(department)
            complaint.department = depart
            complaint.save()
            return redirect('services:homepage')
            #success message
    
    context = {
        'complaints':complaints,
        'departments' : departments,
    }
    
    return render(request, 'app/index.html', context)

# Create your views here.
