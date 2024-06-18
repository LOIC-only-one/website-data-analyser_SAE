# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('releves/', views.releve_list, name='releve_list'),
    # Autres chemins d'URL
]
