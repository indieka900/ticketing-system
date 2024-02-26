from django import forms 
from services.models import Complaint

class CreateComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ("message","file","department")