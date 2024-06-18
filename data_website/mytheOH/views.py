from django.shortcuts import render
from .models import Releve

def releve_list(request):
    relevés = Releve.objects.all()
    return render(request, 'releve_list.html', {'relevés': relevés})
