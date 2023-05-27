from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Caregiver, Patient, Reminder, Speaker, Conversation

class CaregiverAdmin(admin.ModelAdmin):
    pass

class PatientAdmin(admin.ModelAdmin):
    pass

class ReminderAdmin(admin.ModelAdmin):
    pass

class SpeakerAdmin(admin.ModelAdmin):
    pass

class ConversationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Caregiver, CaregiverAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Reminder, ReminderAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Conversation, ConversationAdmin)
