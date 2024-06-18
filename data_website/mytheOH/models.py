# Create your models here.
# models.py
from django.db import models

class Capteur(models.Model):
    capteur_id = models.CharField(max_length=50, primary_key=True)
    nom = models.CharField(max_length=100, unique=True)
    piece = models.CharField(max_length=50)
    emplacement = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nom

class Releve(models.Model):
    releve_id = models.AutoField(primary_key=True)
    capteur = models.ForeignKey(Capteur, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    temperature = models.FloatField()

    def __str__(self):
        return f"{self.capteur.nom} - {self.timestamp} - {self.temperature}"
