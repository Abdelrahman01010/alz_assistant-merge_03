from django.db import models

# Create your models here.
class Caregiver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    audio_path = models.TextField(null=True) ## rem to modify null to false
    caregiver = models.ForeignKey(Caregiver, on_delete=models.SET_NULL, null=True) ##

class Reminder(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    time = models.DateTimeField() 
    caregiver = models.ForeignKey(Caregiver, on_delete=models.DO_NOTHING) ##
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE) ##

class Speaker(models.Model):
    img_path = models.ImageField(upload_to='photos')
    audio_path = models.TextField(null=True)
    is_recognized = models.BooleanField()
    relationship = models.CharField(max_length=255, null=True) 
    recognized_name = models.CharField(max_length=255, null=True) 
    entry_date = models.DateTimeField(auto_now_add=True) 
    caregiver = models.ForeignKey(Caregiver, on_delete=models.DO_NOTHING) ##

class Conversation(models.Model):
    conversation_text = models.TextField()
    summarized_text = models.TextField()
    conversation_timestamp = models.DateTimeField(auto_now_add=True) 
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE) ##
    speaker = models.ForeignKey(Speaker, on_delete=models.PROTECT) ##
    
