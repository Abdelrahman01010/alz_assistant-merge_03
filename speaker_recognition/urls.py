from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('caregiver/',views.MyCargiver_id.as_view()),
    path('patient/',views.Mypatient_id.as_view()),
    path('speakers/',views.SpeakerImageView.as_view()),
    path('patients/',views.PatientImageView.as_view()),
    path('upload/',views.upload_image.as_view()),
    path('caregiverAdd/',views.CaregiverAddNewSpeaker.as_view()),
    path('delete_speaker/<int:speaker_id>/', views.SpeakerDeleteView.as_view(), name='delete_speaker'),
    path('edit_speakers/<int:speaker_id>/', views.SpeakerEdit.as_view(), name='edit_speaker'),
    path('loginCaregiver/',views.caregiverLogin.as_view()),
    path('loginPatient/',views.patientLogin.as_view()),
    path('caregivers/signup/', views.CaregiverSignupView.as_view(), name='caregiver_signup'),
    path('caregiverpatient/signup/',views.CaregiverPatientSignupView.as_view(),name='caregiver_patient_signup'),
    path('patients/signup/',views.PatientSignupView.as_view(),name='patient_signup'),
    path('Gallery/',views.GalleryAddedByCaregiver.as_view()),
    path('login_token_caregiver/',views.Logincaregiver.as_view()),
    path('login_token_patient/',views.Loginpatient.as_view()),
    path('patientAddNewSpeaker/',views.patientAddSpeaker.as_view()),

    #path('hello/',views.hello),
    #path('speakers/<int:id>/',views.SpeakerImageView_id.as_view()),
    #path('Login/',views.login_view),
    #path('hello/', views.HelloView.as_view(), name='hello'),
    #path('yarb/',views.extract_token),
    #path('caregivers/',views.MyCargiver.as_view()),
    # path('caregiver/token/', views.CaregiverTokenObtainPairView.as_view(), name='caregiver_token_obtain_pair'),
    # path('caregiver_speakers/<int:id>',views.GalleryaddedbyCaregiver),
    # path('protected/',views.HelloView.as_view()),
]
