from rest_framework import serializers
from main.models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id', 'title', 'description', 'time', 'caregiver', 'patient']
