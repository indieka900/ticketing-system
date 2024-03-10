import os
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
        'type':type,
    }
    
    return render(request, 'app/index.html', context)


def get_file_type(filename):
        ext = os.path.splitext(filename)[-1].lower()
        if ext == ".jpg" or ext == ".jpeg" or ext == ".png":
            return "Image"
        elif ext == ".docx" or ext == ".doc":
            return "Word Document"
        elif ext == ".pdf":
            return "PDF"
        else:
            return "Unknown"

@login_required
def viewComp(request, pk):
    complaint = Complaint.objects.get(pk=pk)
    
    filename = ""
    if complaint.file:
        filename = filename = os.path.basename(complaint.file.name) 
    file_type = get_file_type(filename)
    context = {
        'complaint': complaint,
        'file_type' : file_type,
    }
    return render(request, 'app/complaint.html', context)

@login_required
def viewFeebacks(request, pk):
    complaint = Complaint.objects.get(pk=pk)
    feedbacks = Feedback.objects.filter(complaint=complaint)
    
    filename = ""
    if complaint.file:
        filename = filename = os.path.basename(complaint.file.name) 
        print(filename)
    file_type = get_file_type(filename)
    
    context = {
        'complaint': complaint,
        'file_type' : file_type,
    }
    return render(request, 'app/feedbacks.html', context)

# Create your views here.
