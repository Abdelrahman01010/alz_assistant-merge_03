from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *

# caregivers/views.py
class CaregiverListCreateView(generics.ListCreateAPIView):
    queryset = Caregiver.objects.all()
    serializer_class = CaregiverSerializer

class CaregiverRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Caregiver.objects.all()
    serializer_class = CaregiverSerializer

class CaregiverCreateView(generics.CreateAPIView):
    queryset = Caregiver.objects.all()
    serializer_class = CaregiverSerializer

class CaregiverUpdateView(generics.UpdateAPIView):
    queryset = Caregiver.objects.all()
    serializer_class = CaregiverSerializer

class CaregiverDestroyView(generics.DestroyAPIView):
    queryset = Caregiver.objects.all()
    serializer_class = CaregiverSerializer

# patients/views.py
class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

# Reminder/views.py
class ReminderListAPIView(generics.ListCreateAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer

class ReminderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer

# Speaker/views.py
class SpeakerListAPIView(generics.ListCreateAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer

class SpeakerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer


# conversation/views.py
class ConversationListCreateView(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class ConversationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer