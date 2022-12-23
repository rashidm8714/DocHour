from django.db import models
from client.models import Client
from django.contrib.auth.models import User

# Create your models here.
class Specialization(models.Model):
    spec = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.spec

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.CharField(max_length=120)
    location = models.CharField(max_length=100)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class Schedule(models.Model):
    doc = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    taken = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return str(self.doc) +" "+ str(self.date)

    
