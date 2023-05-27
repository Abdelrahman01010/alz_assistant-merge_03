from django.contrib.auth.backends import BaseBackend
from main.models import  Caregiver,Patient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

class CaregiverBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            caregiver = Caregiver.objects.get(email=email)
            if caregiver.password == password :
                return caregiver
            else:
                raise AuthenticationFailed('Invalid email or password')
        except Caregiver.DoesNotExist:
             raise AuthenticationFailed('Invalid email or password')
        #return (student, None)
    def get_user(self, user_id):
        try:
            return Caregiver.objects.get(pk=user_id)
        except Caregiver.DoesNotExist:
            return None
    
    def generate_token(self, caregiver):
        refresh = RefreshToken.for_user(caregiver)
        refresh['user_type'] = 'caregiver'
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'caregiver_name':caregiver.first_name,
        }



class PatientBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            patient = Patient.objects.get(email=email)
            if patient.password == password :
                return patient
            else:
                raise AuthenticationFailed('Invalid email or password')
        except Patient.DoesNotExist:
             raise AuthenticationFailed('Invalid email or password')
        #return (student, None)
    def get_user(self, user_id):
        try:
            return Patient.objects.get(pk=user_id)
        except Patient.DoesNotExist:
            return None
    
    def generate_token(self, patient):
        refresh = RefreshToken.for_user(patient)
        refresh['user_type'] = 'patient'
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'patient_name':patient.first_name,
        }
