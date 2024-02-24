from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    
    context = {}
    
    return render(request, 'app/index.html', context)

# Create your views here.
