import os
from typing import Dict, Any, Optional
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from services.models import Complaint, Feedback, Department
from accounts.models import MyUser
from .forms import CreateComplaintForm, CreateFeedbackForm
from .utils import get_file_type

class ComplaintService:
    """Service layer for handling complaint-related business logic."""
    
    @staticmethod
    def get_user_complaints(user: MyUser, complaint_type: str) -> Dict[str, Any]:
        """
        Retrieve complaints based on user role and type.
        
        Args:
            user (MyUser): Current user
            complaint_type (str): Type of complaints to retrieve
        
        Returns:
            Dict containing complaints queryset and related information
        """
        if user.role not in ["Student", "Chairperson"]:
            user.groups.add()
            raise PermissionDenied("Unauthorized access")

        if complaint_type == 'student':
            complaints = Complaint.objects.filter(sender=user)
        elif complaint_type == 'chair':
            department = Department.objects.get(chairperson=user)
            complaints = Complaint.objects.filter(department=department)
        else:
            complaints = Complaint.objects.none()

        return {
            'all_complaints': complaints,
            'solved_tickets': complaints.filter(status='Solved'),
            'pending_tickets': complaints.filter(status='Pending')
        }

@login_required
# @permission_required(['services.view_department', 'services.add_complaint'])
def home(request, type: str):
    """
    Centralized home view for managing complaints.
    
    Handles:
    - Complaint retrieval
    - Complaint status updates
    - Complaint transfers
    - Complaint creation
    """

    '''group1 = Group.objects.get(id=1)
    group2, created = Group.objects.get_or_create(name="Group 2")
    
    # group2.user_set.add(request.user)
    content_type = ContentType.objects.get_for_model(Complaint)

    # Retrieve all permissions for that content type
    permissions = Permission.objects.filter(content_type=content_type)
    
    user_permissions = request.user.get_all_permissions()

    # Display all permissions for the user
    for perm in user_permissions:
        app_label, permission_codename = perm.split(".")
        print(permission_codename)'''

    # Display the permissions
    # for perm in permissions:
    #     print(f"Permission Name: {perm.name}, Codename: {perm.codename}")
    # permissions = group1.permissions.all()

    try:
        complaint_data = ComplaintService.get_user_complaints(request.user, type)
    except PermissionDenied:
        return redirect('accounts:login')

    departments = Department.objects.all()
    
    if request.method == 'POST':
        return _handle_complaint_actions(request, type, complaint_data['all_complaints'])

    context = {
        **complaint_data,
        'departments': departments,
        'type': type,
        **_get_common_context(request.user),
    }
    
    return render(request, 'app/index.html', context)

def _handle_complaint_actions(request, type: str, complaints):
    """
    Handle different complaint-related POST actions.
    
    Args:
        request: HTTP request object
        type: User type (student/chair)
        complaints: Queryset of complaints
    
    Returns:
        HttpResponseRedirect to home page
    """
    action_handlers = {
        'solved': _mark_complaint_solved,
        'transfer': _transfer_complaint,
        'create-comp': _create_complaint,
    }

    for action, handler in action_handlers.items():
        if action in request.POST:
            handler(request, type)
            break

    return redirect(f'/home/{type}/', kwargs={'type': type})

def _mark_complaint_solved(request, type: str):
    """Mark a specific complaint as solved."""
    complaint_id = request.POST.get('id')
    complaint = Complaint.objects.get(pk=complaint_id)
    complaint.status = 'Solved'
    complaint.save()

def _transfer_complaint(request, type: str):
    """Transfer a complaint to a different department."""
    complaint_id = request.POST.get('id')
    department_id = request.POST.get('department')
    
    complaint = Complaint.objects.get(pk=complaint_id)
    complaint.department = Department.objects.get(pk=department_id)
    complaint.save()

def _create_complaint(request, type: str):
    """Create a new complaint."""
    department_id = request.POST.get('department')
    problem_detail = request.POST.get('problemDetail')
    uploaded_file = request.FILES.get('myfile')
    
    department = Department.objects.get(pk=department_id)
    
    complaint_data = {
        'sender': request.user,
        'message': problem_detail,
        'department': department
    }
    
    if uploaded_file:
        complaint_data['file'] = uploaded_file
    
    Complaint.objects.create(**complaint_data)

@login_required
def view_complaint(request, pk: int):
    """
    View details of a specific complaint.
    
    Args:
        request: HTTP request object
        pk: Primary key of the complaint
    """
    complaint = get_object_or_404(Complaint, pk=pk)
    filename = os.path.basename(complaint.file.name) if complaint.file else ""
    
    context = {
        'complaint': complaint,
        'file_type': get_file_type(filename),
        **_get_common_context(request.user),
    }
    return render(request, 'app/complaint.html', context)

@login_required
def view_feedbacks(request, pk: int):
    """
    View and manage feedbacks for a specific complaint.
    
    Args:
        request: HTTP request object
        pk: Primary key of the complaint
    """
    complaint = get_object_or_404(Complaint, pk=pk)
    feedbacks = Feedback.objects.filter(complaint=complaint)
    
    # Mark user's unread feedbacks as read
    feedbacks.filter(receiver=request.user, read=False).update(read=True)

    if request.method == 'POST':
        return _handle_feedback_creation(request, complaint)

    context = {
        'complaint': complaint,
        'feedbacks': feedbacks,
        **_get_common_context(request.user),
    }
    return render(request, 'app/feedbacks.html', context)

def _handle_feedback_creation(request, complaint):
    form = CreateFeedbackForm(request.POST, request.FILES)
    if form.is_valid():
        feedback = form.save(commit=False)
        feedback.complaint = complaint
        
        # Determine receiver based on sender's role
        feedback.receiver = (
            complaint.department.chairperson 
            if request.user == complaint.sender 
            else complaint.sender
        )
        feedback.sender = request.user
        feedback.save()

        return redirect(f"/feedbacks/{complaint.pk}/")

def _get_common_context(user: MyUser) -> Dict[str, Any]:
    user_type = 'student' if user.role == 'Student' else 'chair'
    return {
        'feedback_l': Feedback.objects.filter(receiver=user, read=False),
        'typ': user_type,
    }