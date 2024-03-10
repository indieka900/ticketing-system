from django import forms 
from services.models import Complaint,Feedback

class CreateComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ("message","file","department")
        
class CreateFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("message","file")