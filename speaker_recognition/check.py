from main.models import Speaker, Caregiver,Patient
from django.http import JsonResponse
def check_if_patient_exist(caregiver):
     email_created = Patient.objects.filter(caregiver=caregiver).exists()
     if not email_created:
        return JsonResponse({'error': 'Please create an email for the patient first.'}, status=403)

     return None
