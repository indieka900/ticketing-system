from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from services.models import (Complaint,Feedback,Department)

@login_required
def home(request):
    
    complaints = Complaint.objects.filter(sender = request.user)
    
    if request.method == 'POST':
        if 'solved' in request.POST:
            id = request.POST.get('id')
            complaint = Complaint.objects.get(pk=id)
            complaint.status = 'Solved'
            complaint.save()
            #success message
    
    context = {
        'complaints':complaints
    }
    
    return render(request, 'app/index.html', context)

# Create your views here.
