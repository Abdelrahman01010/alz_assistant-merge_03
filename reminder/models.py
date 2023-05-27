from django.db import models
from main.models import Patient, Caregiver

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    start_date = models.DateTimeField() 
    end_date = models.DateField(null=True)  # New date field
    is_completed = models.BooleanField(default=False)  # New boolean field
    remind = models.IntegerField(null=True)  # New integer field for reminder
    repeat = models.IntegerField(null=True)  # New integer field for repeat
    color = models.IntegerField(null=True)  # New integer field for color
    caregiver = models.ForeignKey(Caregiver, on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
