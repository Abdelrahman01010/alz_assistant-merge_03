from django.urls import path
from . import views
from .views import *
# URLConf
urlpatterns = [
    path('sum/', views.say_hello),
    path('summarize/', views.summarize),
    path('upload_audio/', views.upload_audio),
    path('get_patient_id_by_email/', GetPatientByEmail.as_view()),
    path('get_caregiver_id_by_email/', GetCaregiverByEmail.as_view()),
    path('patient_audio_upload/', PatientAudioUploadView.as_view()),
    path('conv_audio_upload/', ConversationAudioUploadView.as_view()),
    path('check_audio_exists/', check_audio_exists.as_view()),
    path('last_conversation/', LastConversationView.as_view()),
    path('last_speaker_conversation/', views.last_conversation_api),


]
