# caregivers/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('caregivers/', CaregiverListCreateView.as_view(),
         name='caregiver-list-create'),
    path('caregivers/<int:pk>/', CaregiverRetrieveUpdateDestroyView.as_view(),
         name='caregiver-retrieve-update-destroy'),
    path('caregivers/create/', CaregiverCreateView.as_view(),
         name='caregiver-create'),
    path('caregivers/<int:pk>/update/',
         CaregiverUpdateView.as_view(), name='caregiver-update'),
    path('caregivers/<int:pk>/delete/',
         CaregiverDestroyView.as_view(), name='caregiver-delete'),

    path('patients/', PatientListCreateView.as_view(), name='patient_list_create'),
    path('patients/<int:pk>/', PatientRetrieveUpdateDestroyView.as_view(),
         name='patient_retrieve_update_destroy'),

    path('reminders/', ReminderListAPIView.as_view(), name='reminder-list'),
    path('reminders/<int:pk>/', ReminderDetailAPIView.as_view(),
         name='reminder-detail'),

    path('speakers/', SpeakerListAPIView.as_view(), name='speaker-list'),
    path('speakers/<int:pk>/', SpeakerDetailAPIView.as_view(), name='speaker-detail'),

    path('conversations/', ConversationListCreateView.as_view(),
         name='conversation-list-create'),
    path('conversations/<int:pk>/', ConversationRetrieveUpdateDestroyView.as_view(),
         name='conversation-retrieve-update-destroy'),
]
