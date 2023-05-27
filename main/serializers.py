# caregivers/serializers.py
from rest_framework import serializers
from .models import *

class CaregiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caregiver
        fields = ['id', 'first_name', 'last_name', 'email', 'password']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'