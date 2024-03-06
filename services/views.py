from django.shortcuts import render, redirect
from .forms import CreateComplaintForm
from django.contrib.auth.decorators import login_required
from services.models import (Complaint,Feedback,Department)

@login_required
def home(request,type):
    complaints = ''
    if type=='student':
        complaints = Complaint.objects.filter(sender = request.user)
    elif type == 'chair':
        dep = Department.objects.get(chairperson=request.user)
        complaints = Complaint.objects.filter(department = dep)
    departments = Department.objects.all()
    
    solved_tickets = complaints.filter(status='Solved')
    pending_tickets = complaints.filter(status='Pending')
    
    f = CreateComplaintForm()
    
    if request.method == 'POST':
        if 'solved' in request.POST:
            id = request.POST.get('id')
            complaint = Complaint.objects.get(pk=id)
            complaint.status = 'Solved'
            complaint.save()
            return redirect(f'/home/{type}/')
            #success message
            
        if 'transfer' in request.POST:
            id = request.POST.get('id')
            department = request.POST.get('department')
            complaint = Complaint.objects.get(pk=id)
            depart = Department.objects.get(pk=department)
            print(department)
            complaint.department = depart
            complaint.save()
            return redirect(f'/home/{type}/')
        
        if 'create-comp' in request.POST:
            department = request.POST.get('department')
            problem = request.POST.get('problemDetail')
            file = request.FILES.get('myfile')
            depart = Department.objects.get(pk=department)
            if file:
                complaint = Complaint(sender = request.user, message=problem, file=file, department=depart)
            else:
                complaint = Complaint(sender = request.user, message=problem, department=depart)
            complaint.save()
            return redirect(f'/home/{type}/')
            #success message
    
    context = {
        'complaints':complaints,
        'solved':solved_tickets,
        'pending':pending_tickets,
        'departments' : departments,
        'form':f,
    }
    
    return render(request, 'app/index.html', context)

@login_required
def viewComp(request, pk):
    complaint = Complaint.objects.get(pk=pk)
    context = {
        'complaint': complaint,
    }
    return render(request, 'app/complaint.html', context)

# Create your views here.
