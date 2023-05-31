from django.db import models
from main.models import Patient, Caregiver



class Task(models.Model):
    title = models.CharField(max_length=255, null=True)
    note = models.TextField(null=True)
    is_completed = models.IntegerField(null=True)
    date = models.CharField(max_length=255, null=True)
    start_time = models.CharField(max_length=255, null=True)
    end_time = models.CharField(max_length=255, null=True)
    color = models.IntegerField(null=True)
    remind = models.IntegerField(null=True)
    repeat = models.CharField(max_length=255, null=True)
    caregiver = models.ForeignKey(Caregiver, on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)



# # Create your models here.
# class Task(models.Model):
#     title = models.CharField(max_length=50)
#     description = models.CharField(max_length=255)
#     start_date = models.DateTimeField() 
#     end_date = models.DateField(null=True)  # New date field
#     is_completed = models.BooleanField(default=False)  # New boolean field
#     remind = models.IntegerField(null=True)  # New integer field for reminder
#     repeat = models.IntegerField(null=True)  # New integer field for repeat
#     color = models.IntegerField(null=True)  # New integer field for color
#     caregiver = models.ForeignKey(Caregiver, on_delete=models.DO_NOTHING)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
